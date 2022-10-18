"""
Some examples of calling the CLI without any interaction:
python CLI.py --create --name "testmodel" --description "This is a description" --allocator "PriorityAllocator"
--payment-rule "PriorityPaymentRule" --address "Zurich" --neighbouring-tiles 0 --resolution 2 --height 200
--min-height 50 --timesteps 1000 --allocation-period 500 --owner OwnerA 20 PriorityPathBiddingStrategy
PriorityPathValueFunction --summary --skip-save-config --skip-save-simulation --simulate
"""

import argparse
import glob
import json
import os
import random
from typing import Any, Dict, List, Optional, Type

import requests
import yaml
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator, PathValidator

from API import APISimulationConfig, available_allocators, build_json, run_from_config_for_cli
from API.WebClasses import WebAllocator, WebBiddingStrategy
from Development.playground import color_generator
from Simulator import PaymentRule

PREFAB_PATH = "./Prefabs/configs"
HOME_PATH = "~/" if os.name == "posix" else "C:\\"
random.seed(3)


def random_locations_for_bidding_strategy(bidding_strategy: Type["WebBiddingStrategy"]) -> List:
    """
    Returns a list of random path locations with minimum number of locations for
    a given bidding strategy
    :param bidding_strategy: Bidding strategy
    :return: Minimum list of random paths
    """
    return [{"type": "random", "points": []} for _ in range(bidding_strategy.min_locations)]


def bidding_strategy_to_dict(bidding_strategy: Type["WebBiddingStrategy"]):
    """
    Creates a dictionary in the form that is required by the simulation config file from
    a bidding strategy class object
    :param bidding_strategy: Bidding Strategy Class
    :return: Dictionary that is compatible with the simulation config
    """
    return {
        "minLocations": bidding_strategy.min_locations,
        "maxLocations": bidding_strategy.max_locations,
        "allocationType": bidding_strategy.allocation_type,
        "classname": bidding_strategy.__name__,
        "meta": bidding_strategy.meta()
    }


def allocator_from_name(allocator_name: str) -> Type["WebAllocator"]:
    """
    Resolves an allocator class object given the allocators classname
    :param allocator_name: Classname of allocator
    :return: Allocator class object
    """
    allocator_list = list(filter(lambda x: (x.__name__ == allocator_name), available_allocators))
    if len(allocator_list) == 0:
        raise ValueError(f"Allocator '{allocator_name}' unknown")
    return allocator_list[0]


def bidding_strategy_from_name(allocator: Type["WebAllocator"], strategy_name: str) -> Type["WebBiddingStrategy"]:
    """
    Resolves the name of a bidding strategy to the BiddingStrategy class type. If the provided bidding
    strategy name is incompatible with the provided allocator class object, a ValueError is thrown.
    :param allocator: Allocator Class that must match bidding strategy
    :param strategy_name: Classname of bidding strategy
    :return:
    """
    strategies = list(filter(lambda x: (x.__name__ == strategy_name), allocator.compatible_bidding_strategies()))
    if len(strategies) == 0:
        raise ValueError(
            f"Bidding strategy '{strategy_name}' is unknown or incompatible with allocator '{allocator.__name__}'")
    return strategies[0]


def payment_rule_from_name(allocator: Type["WebAllocator"], rule_name: str) -> Type["PaymentRule"]:
    """
    Resolves the name of a payment rule to the PaymentRule class type.The provided payment rule must
    be compatible with the given allocator.
    :param allocator: Allocator Class that must match payment rule
    :param rule_name: Classname of payment rule
    :return:
    """
    rules = list(filter(lambda x: (x.__name__ == rule_name), allocator.compatible_payment_functions()))
    if len(rules) == 0:
        raise ValueError(
            f"Payment rule '{rule_name}' is unknown or incompatible with allocator '{allocator.__name__}'")
    return rules[0]


def available_prefab_names() -> List[str]:
    """
    Returns a list of available prefab simulation configurations
    :return: Prefab names
    """
    file_list = glob.glob(f"{PREFAB_PATH}/*.json")
    return [os.path.basename(file).split("-config")[0] for file in file_list]


def available_allocator_names() -> List[str]:
    """
    Returns a list of allocator names
    :return: Allocator names
    """
    return [allocator.__name__ for allocator in available_allocators]


def all_payment_rule_names() -> List[str]:
    """
    Returns a list of all payment rule names
    :return: Payment Rules
    """
    names = set()
    for allocator in available_allocators:
        names.update([payment_function.__name__ for payment_function in allocator.compatible_payment_functions()])
    return list(names)


def all_payment_rules_str() -> str:
    """
    Returns a nicely formatted string that illustrates the available allocators and their matching
    payment rules
    :return:
    """
    s = ""
    for allocator in available_allocators:
        payment_functions = [payment_function.__name__ for payment_function in allocator.compatible_payment_functions()]
        s += f"{allocator.__name__}: [{', '.join(payment_functions)}]. "
    return s


def all_bidding_strategies_and_value_functions_str() -> str:
    """
    Returns a nicely formatted string that illustrates the available allocators and their matching
    bidding strategies as well as the bidding strategies and their matching value functions.
    :return:
    """
    s = ""
    strategies = set([])
    for allocator in available_allocators:
        bidding_strategies = [bidding_strategy.__name__ for bidding_strategy in
                              allocator.compatible_bidding_strategies()]
        s += f"{allocator.__name__}: [{', '.join(bidding_strategies)}]. "
        strategies.update(allocator.compatible_bidding_strategies())
    for strategy in strategies:
        compatible_value_function_list = [value_function.__name__ for value_function in
                                          strategy.compatible_value_functions()]
        s += f"{strategy.__name__}: [{', '.join(compatible_value_function_list)}]. "
    return s


# The config will be injected into this variable, either through loading it from disk or creating a new one
model_config: Optional[APISimulationConfig] = None

parser = argparse.ArgumentParser(description='Start a new Airspace Auction Simulation')
parser.add_argument('-p', '--prefab', dest="prefab", type=str, metavar=f"[{', '.join(available_prefab_names())}]",
                    help=f'AAS comes with predefined simulation configurations that you can use to test the '
                         f'functionalities of the Simulator. By specifying the name of a prefab, you can load its '
                         f'configuration and run a simulation based of it. You can also save your own configurations '
                         f'as prefabs by placing them into the folder "/Prefabs". The File-name will become the prefab '
                         f'name. Currently ,the following prefabs are available: '
                         f'{", ".join(available_prefab_names())}.')
parser.add_argument('-l', '--load', dest="load_path", type=str,
                    help='You can load your previously saved configuration file by specifying the absolute path to '
                         'your *-config.json File.')
parser.add_argument('-c', '--create', dest="create", action="store_true",
                    help='Flag that tells the CLI to create a new model based on your model configuration. '
                         'Prevents theCLI from asking you whether you want to load a prefab or an already '
                         'existing simulation config file.')
parser.add_argument('-s', '--simulate', dest="simulate", action="store_true",
                    help='Flag that tells the CLI to start a simulation after the model configuration '
                         'file was generated.')
parser.add_argument('-ss', '--skip-simulation', dest="skipSimulation", action="store_true",
                    help='Flag that tells the CLI to not run a simulation. If you want to prevent the CLI '
                         'from asking you interactive questions, please specify either '
                         'the --simulate or --skip-simulation flag.')

parser.add_argument('--summary', dest="summary", action="store_true",
                    help='Flag to output compact summaries of your simulation configuration as well as your '
                         'final simulation output to the console in YAML format')
parser.add_argument('--skip-summary', dest="skipSummary", action="store_true",
                    help='Flag to skip printing the summaries to the console. If you wan to prevent the CLI '
                         'from asking you interactive questions, '
                         'please specify either the --summary or --skip-summary flag.')
parser.add_argument('--save-config', dest="saveConfigPath", type=str,
                    help='Specifies an absolute path to which your simulation configuration will be saved. '
                         'Please only provide a folder, as your configuration will be saved with the naming '
                         'schema {name}-config.json')
parser.add_argument('--skip-save-config', dest="skipSaveConfig", action="store_true",
                    help='Flag that tells the CLI that you do not want to save the configuration to disk. '
                         'This flag is usefull if you want to prevent the CLI from asking you interactively '
                         'whether you want to save your created configuration to your disk.')
parser.add_argument('--save-simulation', dest="saveSimulationPath", type=str,
                    help='Specifies an absolute path to which your final simulation output will be saved. '
                         'Please only provide a folder, as your configuration will be saved with the naming schema '
                         '{name}-simulation.json')
parser.add_argument('--skip-save-simulation', dest="skipSaveSimulation", action="store_true",
                    help='Flag that tells the CLI that you do not want to save the final simulation output to disk. '
                         'This flag is usefull if you want to prevent the CLI from asking you interactively whether '
                         'you want to save your simulation output to your disk.')

parser.add_argument('--name', dest="name", type=str,
                    help='The name of your model. This name will also be included in the filename of your '
                         'configuration and simulation output JSON files. Hence, please only specify valid filename '
                         'characters.')
parser.add_argument('--description', dest="description", type=str,
                    help='Model description. This parameter can be used to describe your model in full details. '
                         'However, there is no need to describe your simulation parameters, as they will all be '
                         'included in the model configuration file as well.')
parser.add_argument('--allocator', dest="allocator", type=str, metavar=f"[{', '.join(available_allocator_names())}]",
                    help=f'The allocator is responsible for allocating paths to agents based on the specified '
                         f'bidding mechanism and payment function. The following allocators are available: '
                         f'{", ".join(available_allocator_names())}.')
parser.add_argument('--payment-rule', dest="paymentRule", type=str, metavar=f"[{', '.join(all_payment_rule_names())}]",
                    help=f'The payment rule specifies how the agents compete for paths in a simulation. Not all '
                         f'allocators can handle all payment rules, though. The following payment rules are '
                         f'available for the supported allocators: {all_payment_rules_str()}')
parser.add_argument('--address', dest="addressQuery", type=str,
                    help='Airspace simulations happen on a real map. By specifying an address here, you can choose '
                         'where your simulation will be centered. You can use any city as an input here, for example '
                         '"Zurich", "New York" or "Barcelona".')
parser.add_argument('--neighbouring-tiles', dest="neighbouringTiles", type=int, choices=range(0, 3), metavar="[0-3]",
                    help='Per default, a ~800m by ~800m region around your address input is used for the '
                         'simulation - for technical reasons. By increasing the amount of neighbouring tiles, '
                         'you can increase the region to 2400m^2, 4000m^2 and 5600m^2.')
parser.add_argument('--resolution', dest="resolution", type=int, choices=range(1, 20), metavar="[1, 20]",
                    help='This parameter lets you specify the resolution of your simulation. Per default, agents '
                         'can navigate through the map with a precision of 1m. By increasing this parameter, your '
                         'agents can navigate less precisely around buildings, but the simulation duration decreases '
                         'drastically.')
parser.add_argument('--height', dest="height", type=int, choices=range(20, 1000), metavar="[20, 1000]",
                    help='The maximum height your agents are allowed to fly')
parser.add_argument('--min-height', dest="minHeight", type=int, choices=range(0, 999), metavar="[20, 999]",
                    help='The minimum height your agents must fly up to before navigating the map. Your agents will '
                         'appear at this height. Usually, this height is set to be slightly higher than the average '
                         'building in your city, since we want to prevent agents to fly accross balconies.')
parser.add_argument('--timesteps', dest="timesteps", type=int, choices=range(300, 4000), metavar="[300, 4000]",
                    help='The number of timesteps you want to run your simulation for. Agents must start and land '
                         'within this timeperiod. The fewer timesteps you simulate, the more agents will be in the '
                         'air at the same time. However, keep in mind that large playfields with fine granularity '
                         'require the agents to fly for longer. Agents that can not reach their destination within '
                         'your specified timesteps will not be allocated.')
parser.add_argument('--allocation-period', dest="allocationPeriod", type=int, choices=range(300, 4000),
                    metavar="[300, 4000]",
                    help='Agents should not be allowed to start their journey in the last timesteps, since they '
                         'will not reach their destination on-time. Hence, you need to specify for how long new '
                         'agents are allowed to enter the playing field. Usually, this parameter should be between '
                         '10 and 33 percent of the total number of timesteps you specified.')

parser.add_argument('--owner', dest="owners", action='append', nargs='+', default=[],
                    metavar="[Name, nAgents, BiddingStrategy, ValueFunction]",
                    help="Owners act according to a bidding strategy and to maximize their value functions. They spawn "
                         "agents on the playing field and act on their best interrest. Owners will spaws agents at "
                         "random locations. To have further control over where owners spawn agents and the paths they "
                         "fly, use the Web-UI. To create a new owner, specify the following information in the right "
                         "order: Name(str), nAgents(int), BiddingStrategy(str), ValueFunction(str). You can call this "
                         "argument multiple times to create multiple owners. Note that not all BiddingStrategies are "
                         "compatible with all Allocators and not all ValueFunctions are compatible with all "
                         "BiddingStrategies. The supported pairs are listed here. "
                         f"{all_bidding_strategies_and_value_functions_str()}")

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
# Skip this interaction if user provides 'create' argument
if model_config is None and not args.create:
    use_prefab = inquirer.confirm(message="Use prefab configuration?", default=True).execute()
    if use_prefab:
        files = glob.glob(f"{PREFAB_PATH}/*.json")
        prefab = inquirer.select(
            message="Select a prefab:",
            choices=[Choice(file, name=os.path.basename(file)) for file in files],
            default=None,
        ).execute()
        with open(prefab, "r") as f:
            model_config = APISimulationConfig(**json.load(f))

# No argument led to creation of a model and no prefab was selected - ask user if model should be loaded
# Skip this interaction if user provides 'create' argument
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
    model_data: Dict[str, Any] = {
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
            "biddingStrategy": bidding_strategy_to_dict(
                bidding_strategy_from_name(allocator_from_name(args.allocator), owner[2])),
            "valueFunction": owner[3],
            "locations": random_locations_for_bidding_strategy(
                bidding_strategy_from_name(allocator_from_name(args.allocator), owner[2])),
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

    # Convert provided address query argument to location and coordinates
    if args.addressQuery:
        data = requests.get(
            f"https://nominatim.openstreetmap.org/search?q={args.addressQuery}&format=json&addressdetails=1").json()
        if data is None or len(data) == 0:
            raise ValueError(f"Unable to resolve address for query '{args.addressQuery}'")
        model_data["map"]["locationName"] = data[0]["display_name"]
        model_data["map"]["coordinates"]["lat"] = float(data[0]["lat"])
        model_data["map"]["coordinates"]["long"] = float(data[0]["lon"])
    else:
        # Interactively ask the user for a query and prompt him whether the resolved location is correct
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

    if model_data["map"]["minHeight"] is None:
        model_data["map"]["minHeight"] = int(inquirer.number(
            message="Minimum flight height:",
            min_allowed=0,
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
            max_allowed=round(model_data["map"]["timesteps"] / 2),
            validate=EmptyInputValidator(),
        ).execute())

    # Interactively ask for owner data until at least 1 owner exists and until the user breaks the flow
    if not len(model_data["owners"]) > 0:
        add_owner = True
        while add_owner:
            i = len(model_data["owners"]) + 1

            owner_name = inquirer.text(message=f"Owner {i} - Name:", validate=EmptyInputValidator()).execute()
            owner_agents = int(inquirer.number(
                message=f"Owner {i} - Number of Agents:",
                min_allowed=1,
                max_allowed=100,
                validate=EmptyInputValidator(),
            ).execute())

            owner = {
                "color": color_generator(),
                "name": owner_name,
                "agents": owner_agents,
                "biddingStrategy": None,
                "valueFunction": "",
            }

            # Ask user for choice within bidding strategies that are compatible with selected allocator
            allocators = list(filter(lambda x: (x.__name__ == model_data["allocator"]), available_allocators))
            selected_allocator = allocators[0]
            compatible_bidding_strategies = selected_allocator.compatible_bidding_strategies()
            owner['biddingStrategy'] = inquirer.select(
                message=f"Owner {i} - Bidding Strategy:",
                choices=[Choice(bidding_strategy_to_dict(bidding_strategy), name=bidding_strategy.__name__) for
                         bidding_strategy in compatible_bidding_strategies],
                validate=EmptyInputValidator(),
            ).execute()
            selected_bidding_strategy = bidding_strategy_from_name(selected_allocator,
                                                                   owner['biddingStrategy']['classname'])

            # Ask user for choice within value functions that are compatible with selected allocator
            compatible_value_functions = selected_bidding_strategy.compatible_value_functions()
            owner['valueFunction'] = inquirer.select(
                message=f"Owner {i} - Value Function:",
                choices=[Choice(value_function.__name__) for value_function in compatible_value_functions],
                validate=EmptyInputValidator(),
            ).execute()

            # Generate random location for selected bidding strategies
            # The CLI could be extended in the future to make configurations of paths possible, such as
            # Number of stops for path agens or dimensions of space agents.
            # Even selection of locations or heatmap inputs could be extended in the future.
            # As of right now, these are only supported by the Web-UI since the complexitiy of the CLI should be
            # kept to an easily understandable extend.
            owner["locations"] = random_locations_for_bidding_strategy(selected_bidding_strategy)
            print(f"----- OWNER {i} -----")
            print(
                f"{owner['name']} {owner['agents']} {owner['biddingStrategy']['classname']} {owner['valueFunction']}")
            print("--------------------")
            model_data["owners"].append(owner)
            add_owner = inquirer.confirm(message="Add another owner?", default=True).execute()

    model_config = APISimulationConfig(**model_data)

# Ask for model summary if user did not specify either --summary or --skip-summary
if not args.skipSummary:
    summarize = args.summary
    if not summarize:
        summarize = inquirer.confirm(message="Print model summary?", default=True).execute()
    if summarize:
        print("===================== CONFIG SUMMARY ========================")
        print(yaml.dump(model_config.dict(), sort_keys=False))
        print("=============================================================")

# Save config flow if user did not specify --skip-save-config
if not args.skipSaveConfig:
    save_model = args.saveConfigPath
    # Only ask the user for config path if he did not already specify one
    if not save_model:
        save_model = inquirer.confirm(message="Save model configuration?", default=True).execute()
    # Enter this flow if user provided a path or responded with "yes" in the previous step
    if save_model:
        dest_path = args.saveConfigPath
        # Ask user for config path if not already provided as input parameter
        if not dest_path:
            dest_path = inquirer.filepath(
                message="Folder:",
                default=HOME_PATH,
                validate=PathValidator(is_dir=True, message="Input is not a directory"),
                only_directories=True,
            ).execute()
        output_path = dest_path if dest_path.endswith(".json") else os.path.join(dest_path,
                                                                                 f"{model_config.name}-config.json")
        # Write config as to disk as json file
        with open(output_path, "w") as f:
            f.write(model_config.json())

# Skip this flow if user provided --skip-simulation argument
if not args.skipSimulation:
    # Ask user if simulation should be run if he provided neither --skip-simulation nor --simulate
    simulate = True
    if not args.simulate:
        simulate = inquirer.confirm(message="Start Simulation?", default=True).execute()
    # Run actual simulation
    if simulate:
        print("Running simulation. This may take a while!")
        generator, duration = run_from_config_for_cli(model_config)
        print(f"-- Simulation Completed in {duration} seconds --")
        simulation_json = build_json(model_config.dict(), generator, duration)

        # Printing simulation summary flow if user did not provide --skip-summary flag
        if not args.skipSummary:
            # If user did neither provide --summary nor --skip-summary, ask for his input
            summarize = args.summary
            if not summarize:
                summarize = inquirer.confirm(message="Print simulation summary?", default=True).execute()
            # Print summary as YAML (for better readability and more compact output)
            if summarize:
                print("===================== SIMULATION SUMMARY ========================")
                print(yaml.dump(simulation_json, sort_keys=False))
                print("=================================================================")

        # Save simulation flow if --skip-save-simulation is not provided
        if not args.skipSaveSimulation:
            save_simulation = args.saveSimulationPath
            # If user did neither provide --save-simulation-path nor --skip-save-simulation, ask for his input
            if not save_simulation:
                save_simulation = inquirer.confirm(message="Save simulation?", default=True).execute()
            # If path is present or user responded with 'yes', save simulation
            if save_simulation:
                dest_path = args.saveSimulationPath
                if not dest_path:
                    dest_path = inquirer.filepath(
                        message="Folder:",
                        default=HOME_PATH,
                        validate=PathValidator(is_dir=True, message="Input is not a directory"),
                        only_directories=True,
                    ).execute()
                # Save simulation to disk
                output_path = dest_path if dest_path.endswith(".json") else f"{model_config.name}-simulation.json"
                with open(os.path.join(dest_path, output_path), "w") as f:
                    json.dump(simulation_json, f, indent=4)
