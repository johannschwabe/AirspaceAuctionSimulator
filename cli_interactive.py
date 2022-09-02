import json
import os
import glob
import argparse

import requests
from pyproj import Proj, transform
import yaml
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator, EmptyInputValidator

from API.config import available_allocators
from API.Types import APISimulationConfig

PREFAB_PATH = "./Prefabs/configs"
HOME_PATH = "~/" if os.name == "posix" else "C:\\"

model = None

parser = argparse.ArgumentParser(description='Start a new Airspace Auction Simulation')
parser.add_argument('-p', '--prefab', dest="prefab", type=str, help='Prefab Name')
parser.add_argument('-l', '--load', dest="load_path", type=str, help='File path to configuration to load')
parser.add_argument('-c', '--create', dest="create", action="store_true", help='Create a new model')

parser.add_argument('-n', '--name', dest="name", type=str, help='Model name')
parser.add_argument('-d', '--description', dest="description", type=str, help='Model description')
parser.add_argument('--allocator', dest="allocator", type=str, help='Allocator')
parser.add_argument('--address', dest="addressQuery", type=str, help='Address Query')
parser.add_argument('--neighbouring-tiles', dest="neighbouringTiles", type=int, choices=range(0, 3), help='Neighbouring Tiles for Map')
parser.add_argument('--resolution', dest="resolution", type=int, choices=range(1, 20), help='Map resolution')
parser.add_argument('--height', dest="height", type=int, choices=range(20, 1000), help='Map height')
parser.add_argument('--timesteps', dest="timesteps", type=int, choices=range(300, 4000), help='Timesteps')

args = parser.parse_args()

# Load prefab model specified by arguments
if args.prefab:
    with open(f"{PREFAB_PATH}/{args.prefab}-config.json", "r") as f:
        model = APISimulationConfig(**json.load(f))

# Load model from path specified by arguments
if args.load_path:
    with open(args.load_path, "r") as f:
        model = APISimulationConfig(**json.load(f))

# No argument led to creation of a model - ask user if prefab should be used
if model is None and not args.create:
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

# No argument led to creation of a model and no prefab was selected - ask user if model should be loaded
if model is None and not args.create:
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

# No model was generated to this point - generate new model
if model is None:
    model_data = {
        "name": args.name,
        "description": args.description,
        "allocator": args.allocator,
        "map": {
            "coordinages": {
                "lat": -1.0,
                "long": -1.0,
            },
            "locationName": "",
            "neighbouringTiles": args.neighbouringTiles,
            "bottomLeftCoordinate": {
                "lat": -1.0,
                "long": -1.0,
            },
            "topRightCoordinate": {
                "lat": -1.0,
                "long": -1.0,
            },
            "resolution": args.resolution,
            "height": args.height,
            "timesteps": args.timesteps,
        }
    }
    if not model_data['name']:
        model_data['name'] = inquirer.text(message="Model Name:", validate=EmptyInputValidator()).execute()

    if not model_data['description']:
        model_data['description'] = inquirer.text(message="Model Description:",
                                                  validate=EmptyInputValidator()).execute()

    if not model_data['allocator']:
        model_data['allocator'] = inquirer.select(
            message="Allocator:",
            choices=[Choice(allocator.__name__) for allocator in available_allocators],
            default=None,
        ).execute()

    if args.addressQuery:
        data = requests.get(
            f"https://nominatim.openstreetmap.org/search?q={args.addressQuery}&format=json&addressdetails=1").json()
        if data is None or len(data) == 0:
            raise ValueError(f"Unable to resolve address for query '{args.addressQuery}'")
        model_data["map"]["locationName"] = data[0]["display_name"]
        model_data["map"]["coordinages"]["lat"] = float(data[0]["lat"])
        model_data["map"]["coordinages"]["long"] = float(data[0]["lon"])
    else:
        address_correct = False
        while not address_correct:
            addressQuery = inquirer.text(message="Location:", validate=EmptyInputValidator()).execute()
            data = requests.get(
                f"https://nominatim.openstreetmap.org/search?q={addressQuery}&format=json&addressdetails=1").json()
            if data is None or len(data) == 0:
                print("Could not find any address for given query. Try again!")
            else:
                model_data["map"]["locationName"] = data[0]["display_name"]
                model_data["map"]["coordinages"]["lat"] = float(data[0]["lat"])
                model_data["map"]["coordinages"]["long"] = float(data[0]["lon"])
                print(f"Found address '{model_data['map']['locationName']}'")
                address_correct = inquirer.confirm(message="Location correct?", default=True).execute()

    model_data["map"]["neighbouringTiles"] = inquirer.number(
        message="Neighbouring Tiles:",
        min_allowed=0,
        max_allowed=3,
        validate=EmptyInputValidator(),
    ).execute()

    # TODO bottomLeftCoordinate
    # TODO topRightCoordinate
    # lat = float(model_data["map"]["coordinages"]["lat"])
    # lon = float(model_data["map"]["coordinages"]["lon"])
    # transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), lon, lat)

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
