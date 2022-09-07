from typing import Dict, Type, List

import json
import os
import glob
import argparse

import requests
import yaml
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator, EmptyInputValidator

from API import run_from_config
from API.config import available_allocators
from API.Types import APISimulationConfig
from Development.playground import color_generator
from Simulator.IO.JSONS import build_json

from Simulator.Mechanism.Allocator import Allocator
from Simulator.Bids.BiddingStrategy import BiddingStrategy
from Simulator.Mechanism.PaymentRule import PaymentRule


def random_locations_for_bidding_strategy(bidding_strategy: Type[BiddingStrategy]) -> List:
    return [{ "type": "random", "points": [] } for _ in range(bidding_strategy.min_locations)]

def bidding_strategy_to_dict(bidding_strategy: Type[BiddingStrategy]):
    return {
        "minLocations": bidding_strategy.min_locations,
        "maxLocations": bidding_strategy.max_locations,
        "allocationType": bidding_strategy.allocation_type,
        "classname": bidding_strategy.__name__,
        "meta": bidding_strategy.meta()
    }

def bidding_strategy_from_name(allocator: Type[Allocator], bidding_strategy_name: str) -> Type[BiddingStrategy]:
    allocators = list(filter(lambda x: (x.__name__ == allocator), available_allocators))
    selected_allocator = allocators[0]
    compatible_bidding_strategies = selected_allocator.compatible_bidding_strategies()
    bidding_strategy = list(filter(lambda b: (b.__name__ == bidding_strategy_name), compatible_bidding_strategies))
    if len(bidding_strategy) == 0:
        raise ValueError(
            f"Bidding strategy '{bidding_strategy_name}' is unknown or incompatible with allocator '{allocator.__name__}'")
    return bidding_strategy[0]


def allocator_from_name(allocator_name: str) -> Type[Allocator]:
    allocators = list(filter(lambda x: (x.__name__ == allocator_name), available_allocators))
    if len(allocators) == 0:
        raise ValueError(f"Allocator '{allocator_name}' unknown")
    return allocators[0]


def bidding_strategy_by_name(allocator: Type[Allocator], strategy_name: str) -> Type[BiddingStrategy]:
    strategies = list(filter(lambda x: (x.__name__ == strategy_name), allocator.compatible_bidding_strategies()))
    if len(strategies) == 0:
        raise ValueError(
            f"Bidding strategy '{strategy_name}' is unknown or incompatible with allocator '{allocator.__name__}'")
    return strategies[0]


def payment_rule_by_name(allocator: Type[Allocator], rule_name: str) -> Type[PaymentRule]:
    rules = list(filter(lambda x: (x.__name__ == rule_name), allocator.compatible_payment_functions()))
    if len(rules) == 0:
        raise ValueError(
            f"Payment rule '{rule_name}' is unknown or incompatible with allocator '{allocator.__name__}'")
    return rules[0]


PREFAB_PATH = "./Prefabs/configs"
HOME_PATH = "~/" if os.name == "posix" else "C:\\"

model_config = None

parser = argparse.ArgumentParser(description='Start a new Airspace Auction Simulation')
parser.add_argument('-p', '--prefab', dest="prefab", type=str, help='Prefab Name')
parser.add_argument('-l', '--load', dest="load_path", type=str, help='File path to configuration to load')
parser.add_argument('-c', '--create', dest="create", action="store_true", help='Create a new model')
parser.add_argument('-s', '--simulate', dest="simulate", action="store_true", help='Start simulation')
parser.add_argument('-ss', '--skip-simulation', dest="skipSimulation", action="store_true", help='Skip simulation')

parser.add_argument('--summary', dest="summary", action="store_true", help='Log summary of created config file')
parser.add_argument('--skip-summary', dest="skipSummary", action="store_true",
                    help='Do not log summary of created config file')
parser.add_argument('--save-config', dest="saveConfigPath", type=str, help='Path to save model config file to')
parser.add_argument('--save-simulation', dest="saveSimulationPath", type=str, help='Path to save simulation to')
parser.add_argument('--skip-save-config', dest="skipSaveConfig", action="store_true",
                    help='Do not save config file to disk')
parser.add_argument('--skip-save-simulation', dest="skipSaveSimulation", action="store_true",
                    help='Do not save simulation file to disk')

parser.add_argument('--name', dest="name", type=str, help='Model name')
parser.add_argument('--description', dest="description", type=str, help='Model description')
parser.add_argument('--allocator', dest="allocator", type=str, help='Allocator')
parser.add_argument('--payment-rule', dest="paymentRule", type=str, help='Payment Rule')
parser.add_argument('--address', dest="addressQuery", type=str, help='Address Query')
parser.add_argument('--neighbouring-tiles', dest="neighbouringTiles", type=int, choices=range(0, 3),
                    help='Neighbouring Tiles for Map')
parser.add_argument('--resolution', dest="resolution", type=int, choices=range(1, 20), help='Map resolution')
parser.add_argument('--height', dest="height", type=int, choices=range(20, 1000), help='Map height')
parser.add_argument('--min-height', dest="minHeight", type=int, choices=range(20, 999), help='Minimum Flight height')
parser.add_argument('--timesteps', dest="timesteps", type=int, choices=range(300, 4000), help='Timesteps')
parser.add_argument('--allocation-period', dest="allocationPeriod", type=int, choices=range(300, 4000),
                    help='Allocation period')

parser.add_argument('--owner', dest="owners", action='append', nargs='+', default=[],
                    help="Configuration of owner: Name, agents, BiddingStrategy, ValueFunction")

args = parser.parse_args()

# Pre-Checks
# If owners are given, bidding strategies must be set
assert len(
    args.owners) == 0 or args.allocator, "Allocator (--allocator) argument is required if owners are given as args"

# Load prefab model specified by arguments
if args.prefab:
    with open(f"{PREFAB_PATH}/{args.prefab}-config.json", "r") as f:
        model_config = APISimulationConfig(**json.load(f))

# Load model from path specified by arguments
if args.load_path:
    with open(args.load_path, "r") as f:
        model_config = APISimulationConfig(**json.load(f))

# No argument led to creation of a model - ask user if prefab should be used
if model_config is None and not args.create:
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
            model_config = APISimulationConfig(**json.load(f))

# No argument led to creation of a model and no prefab was selected - ask user if model should be loaded
if model_config is None and not args.create:
    load_config = inquirer.confirm(message="Load Simulation from existing config File?", default=True).execute()
    if load_config:
        path_to_simulation_config = inquirer.filepath(
            message="Enter path to simulation config file:",
            default=HOME_PATH,
            validate=PathValidator(is_file=True, message="Input is not a file"),
            only_files=True,
        ).execute()
        with open(path_to_simulation_config, "r") as f:
            model_config = APISimulationConfig(**json.load(f))

# No model was generated to this point - generate new model
if model_config is None:
    model_data = {
        "name": args.name,
        "description": args.description,
        "allocator": args.allocator,
        "paymentRule": args.paymentRule,
        "map": {
            "coordinates": {
                "lat": -1.0,
                "long": -1.0,
            },
            "locationName": "",
            "neighbouringTiles": args.neighbouringTiles,
            "resolution": args.resolution,
            "height": args.height,
            "minHeight": args.minHeight,
            "timesteps": args.timesteps,
            "allocationPeriod": args.allocationPeriod,
        },
        "owners": [{
            "color": color_generator(),
            "name": owner[0],
            "agents": int(owner[1]),
            "biddingStrategy": bidding_strategy_to_dict(bidding_strategy_from_name(args.allocator, owner[2])),
            "valueFunction": owner[3],
            "locations": random_locations_for_bidding_strategy(bidding_strategy_from_name(args.allocator, owner[2])),
        } for owner in args.owners],
    }
    if model_data['name'] is None:
        model_data['name'] = inquirer.text(message="Model Name:", validate=EmptyInputValidator()).execute()

    if model_data['description'] is None:
        model_data['description'] = inquirer.text(message="Model Description:",
                                                  validate=EmptyInputValidator()).execute()

    if model_data['allocator'] is None:
        model_data['allocator'] = inquirer.select(
            message="Allocator:",
            choices=[Choice(allocator.__name__) for allocator in available_allocators],
            validate=EmptyInputValidator()
        ).execute()

    if model_data['paymentRule'] is None:
        selected_allocator = allocator_from_name(model_data['allocator'])
        available_payment_functions = selected_allocator.compatible_payment_functions()
        model_data['paymentRule'] = inquirer.select(
            message="Payment Rule:",
            choices=[Choice(payment_function.__name__) for payment_function in available_payment_functions],
            validate=EmptyInputValidator()
        ).execute()

    if args.addressQuery:
        data = requests.get(
            f"https://nominatim.openstreetmap.org/search?q={args.addressQuery}&format=json&addressdetails=1").json()
        if data is None or len(data) == 0:
            raise ValueError(f"Unable to resolve address for query '{args.addressQuery}'")
        model_data["map"]["locationName"] = data[0]["display_name"]
        model_data["map"]["coordinates"]["lat"] = float(data[0]["lat"])
        model_data["map"]["coordinates"]["long"] = float(data[0]["lon"])
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
                model_data["map"]["coordinates"]["lat"] = float(data[0]["lat"])
                model_data["map"]["coordinates"]["long"] = float(data[0]["lon"])
                print(f"Found address '{model_data['map']['locationName']}'")
                address_correct = inquirer.confirm(message="Location correct?", default=True).execute()

    if model_data["map"]["neighbouringTiles"] is None:
        model_data["map"]["neighbouringTiles"] = int(inquirer.number(
            message="Neighbouring Tiles:",
            min_allowed=0,
            max_allowed=3,
            validate=EmptyInputValidator(),
        ).execute())

    if model_data["map"]["resolution"] is None:
        model_data["map"]["resolution"] = int(inquirer.number(
            message="Resolution:",
            min_allowed=1,
            max_allowed=20,
            validate=EmptyInputValidator(),
        ).execute())

    if model_data["map"]["height"] is None:
        model_data["map"]["height"] = int(inquirer.number(
            message="Maximum flight height:",
            min_allowed=20,
            max_allowed=1000,
            validate=EmptyInputValidator(),
        ).execute())
        print(model_data["map"]["height"], type(model_data["map"]["height"]))

    if model_data["map"]["minHeight"] is None:
        model_data["map"]["minHeight"] = int(inquirer.number(
            message="Minimum flight height:",
            min_allowed=20,
            max_allowed=model_data["map"]["height"] - 1,
            validate=EmptyInputValidator(),
        ).execute())

    if model_data["map"]["timesteps"] is None:
        model_data["map"]["timesteps"] = int(inquirer.number(
            message="Timesteps:",
            min_allowed=300,
            max_allowed=4000,
            validate=EmptyInputValidator(),
        ).execute())

    if model_data["map"]["allocationPeriod"] is None:
        model_data["map"]["allocationPeriod"] = int(inquirer.number(
            message="Allocation Period:",
            min_allowed=1,
            max_allowed=round(model_data["map"]["timesteps"] ** (1 / 3)),
            validate=EmptyInputValidator(),
        ).execute())

    if not len(model_data["owners"]) > 0:
        add_owner = True
        while add_owner:
            i = len(model_data["owners"]) + 1
            owner = {
                "color": color_generator(),
                "name": "",
                "agents": -1,
                "biddingStrategy": None,
                "valueFunction": "",
            }
            owner['name'] = inquirer.text(message=f"Owner {i} - Name:", validate=EmptyInputValidator()).execute()
            owner['agents'] = int(inquirer.number(
                message=f"Owner {i} - Number of Agents:",
                min_allowed=1,
                max_allowed=100,
                validate=EmptyInputValidator(),
            ).execute())
            allocators = list(filter(lambda x: (x.__name__ == model_data["allocator"]), available_allocators))
            selected_allocator = allocators[0]
            compatible_bidding_strategies = selected_allocator.compatible_bidding_strategies()
            owner['biddingStrategy'] = inquirer.select(
                message=f"Owner {i} - Bidding Strategy:",
                choices=[Choice(bidding_strategy_to_dict(bidding_strategy), name=bidding_strategy.__name__) for
                         bidding_strategy in compatible_bidding_strategies],
                validate=EmptyInputValidator(),
            ).execute()
            selected_bidding_strategy = bidding_strategy_by_name(selected_allocator, owner['biddingStrategy']['classname'])
            compatible_value_functions = selected_bidding_strategy.compatible_value_functions()
            owner['valueFunction'] = inquirer.select(
                message=f"Owner {i} - Value Function:",
                choices=[Choice(value_function.__name__) for value_function in compatible_value_functions],
                validate=EmptyInputValidator(),
            ).execute()
            owner["locations"] = random_locations_for_bidding_strategy(selected_bidding_strategy)
            print(f"----- OWNER {i} -----")
            print(
                f"{owner['name']} {owner['agents']} {owner['biddingStrategy']['classname']} {owner['valueFunction']}")
            print("--------------------")
            model_data["owners"].append(owner)
            add_owner = inquirer.confirm(message="Add another owner?", default=True).execute()

    model_config = APISimulationConfig(**model_data)

if not args.skipSummary:
    if not args.summary:
        summarize = inquirer.confirm(message="Print model summary?", default=True).execute()
    if args.summary or summarize:
        print("===================== CONFIG SUMMARY ========================")
        print(yaml.dump(model_config.dict(), sort_keys=False))
        print("=============================================================")

if not args.skipSaveConfig:
    if not args.saveConfigPath:
        save_model = inquirer.confirm(message="Save model configuration?", default=True).execute()
    if args.saveConfigPath or save_model:
        if not args.saveConfigPath:
            input_path = inquirer.filepath(
                message="Folder:",
                default=HOME_PATH,
                validate=PathValidator(is_dir=True, message="Input is not a directory"),
                only_directories=True,
            ).execute()
        dest_path = args.saveConfigPath if args.saveConfigPath else input_path
        with open(os.path.join(dest_path, f"{model_config.name}-config.json"), "w") as f:
            f.write(model_config.json())

if not args.skipSimulation:
    if not args.simulate:
        simulate = inquirer.confirm(message="Start Simulation?", default=True).execute()
    if args.simulate or simulate:
        print("Running simulation. This may take a while!")
        generator, duration = run_from_config(model_config)
        print(f"-- Simulation Completed in {duration} seconds --")
        simulation_json = build_json(generator.simulator, duration)
        simulation_json["config"] = model_config

        if not args.skipSummary:
            if not args.summary:
                summarize = inquirer.confirm(message="Print simulation summary?", default=True).execute()
            if args.summary or summarize:
                print("===================== SIMULATION SUMMARY ========================")
                print(yaml.dump(simulation_json, sort_keys=False))
                print("=================================================================")

        if not args.skipSaveSimulation:
            if not args.saveSimulationPath:
                save_simulation = inquirer.confirm(message="Save simulation?", default=True).execute()
            if args.saveSimulationPath or save_simulation:
                if not args.saveSimulationPath:
                    input_path = inquirer.filepath(
                        message="Folder:",
                        default=HOME_PATH,
                        validate=PathValidator(is_dir=True, message="Input is not a directory"),
                        only_directories=True,
                    ).execute()
                dest_path = args.saveSimulationPath if args.saveSimulationPath else input_path
                with open(os.path.join(dest_path, f"{model_config.name}-config.json"), "w") as f:
                    json.dump(simulation_json, f)

