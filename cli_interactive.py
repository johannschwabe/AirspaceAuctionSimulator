import json
import os
import glob

import requests
from prompt_toolkit.shortcuts import ProgressBar
import yaml
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator, EmptyInputValidator

from API.config import available_allocators
from API.Types import APISimulationConfig

PREFAB_PATH = "./Prefabs/configs"
HOME_PATH = "~/" if os.name == "posix" else "C:\\"

model = None

use_prefab = inquirer.confirm(message="Use prefab configuration?", default=True).execute()
if use_prefab:
    files = glob.glob(f"{PREFAB_PATH}/*.json")
    print(files)
    prefab = inquirer.select(
        message="Select a prefab:",
        choices=[Choice(file, name=os.path.basename(file)) for file in files],
        default=None,
    ).execute()
    with open(prefab, "r") as f:
        model = APISimulationConfig(**json.load(f))
else:
    load_config = inquirer.confirm(message="Load Simulation from existing config File?", default=True).execute()
    if load_config:
        path_to_simulation_config = inquirer.filepath(
            message="Enter path to simulation config file:",
            default=HOME_PATH,
            validate=PathValidator(is_file=True, message="Input is not a file"),
            only_files=True,
        ).execute()
        with open(path_to_simulation_config, "r") as f:
            model = APISimulationConfig(**json.load(f))

    else:
        model_data = {
            "name": "",
            "description": "",
            "allocator": "",
            "map": {
                "locationName": "",
                "coordinages": {
                    "lat": -1.0,
                    "long": -1.0,
                },
                "neighbouringTiles": 0,
                "resolution": 0,
                "height": 0,
                "timesteps": 0,
            }
        }
        model_data['name'] = inquirer.text(message="Model Name:", validate=EmptyInputValidator()).execute()
        model_data['description'] = inquirer.text(message="Model Description:", validate=EmptyInputValidator()).execute()
        model_data['allocator'] = inquirer.select(
            message="Allocator:",
            choices=[Choice(allocator.__name__) for allocator in available_allocators],
            default=None,
        ).execute()

        address_correct = False
        while not address_correct:
            addressQuery = inquirer.text(message="Location:", validate=EmptyInputValidator()).execute()
            data = requests.get(f"https://nominatim.openstreetmap.org/search?q={addressQuery}&format=json&addressdetails=1").json()
            if data is None or len(data) == 0:
                print("Could not find any address for given query. Try again!")
            else:
                model_data["map"]["locationName"] = data[0].display_name
                model_data["map"]["coordinages"]["lat"] = float(data[0].lat)
                model_data["map"]["coordinages"]["long"] = float(data[0].long)
                print(f"Found address {model_data['map']['locationName']}")
                address_correct = inquirer.confirm(message="Location correct?", default=True).execute()

        model_data["map"]["neighbouringTiles"] = inquirer.number(
            message="Neighbouring Tiles:",
            min_allowed=0,
            max_allowed=3,
            validate=EmptyInputValidator(),
        ).execute()

        # TODO bottomLeftCoordinate
        # TODO topRightCoordinate
        # TODO subselection
        model_data["map"]["resolution"] = inquirer.number(
            message="Resolution:",
            min_allowed=1,
            max_allowed=20,
            validate=EmptyInputValidator(),
        ).execute()

        # TODO tiles

        model_data["map"]["height"] = inquirer.number(
            message="Height:",
            min_allowed=20,
            max_allowed=1000,
            validate=EmptyInputValidator(),
        ).execute()

        model_data["map"]["timesteps"] = inquirer.number(
            message="Timesteps:",
            min_allowed=300,
            max_allowed=4000,
            validate=EmptyInputValidator(),
        ).execute()

        model = APISimulationConfig(**model_data)

summarize = inquirer.confirm(message="Print model summary?", default=True).execute()
if summarize:
    print(yaml.dump(model.dict(), sort_keys=False))

save_model = inquirer.confirm(message="Save model configuration?", default=True).execute()
if save_model:
    dest_path = inquirer.filepath(
        message="Folder:",
        default=HOME_PATH,
        validate=PathValidator(is_dir=True, message="Input is not a directory"),
        only_directories=True,
    ).execute()
    with open(os.path.join(dest_path, f"{model.name}-config.json"), "w") as f:
        f.write(model.json())
