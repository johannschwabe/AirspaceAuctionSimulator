import json
import math
import random
import time

from API import APIWorldCoordinates, Area, EnvironmentGen, MapTile, generate_config
from API.GridLocation.GridLocation import GridLocation
from API.GridLocation.GridLocationType import GridLocationType
from API.WebClasses import WebPathOwner, WebSpaceOwner
from Demos.FCFS import FCFSAllocator, FCFSPathBiddingStrategy, FCFSPathValueFunction, FCFSPaymentRule, \
    FCFSSpaceBiddingStrategy, FCFSSpaceValueFunction
from Demos.Priority import PriorityAllocator, PriorityPathBiddingStrategy, PriorityPathValueFunction, \
    PriorityPaymentRule, PrioritySpaceBiddingStrategy, PrioritySpaceValueFunction
from Simulator import Coordinate3D, Coordinate4D, Environment, JSONOwnerDescription, Mechanism, Simulator, \
    StaticBlocker, get_simulation_dict, get_statistics_dict

random.seed(4)
dimensions = Coordinate4D(40, 40, 40, 1000)
allocation_period = 100
space_dimensions = Coordinate4D(7, 7, 7, 10)
nr_agents = 30


def setup_empty():
    blocker = StaticBlocker(Coordinate3D(10, 0, 10), Coordinate3D(20, 20, 20))
    return Environment(dimensions, blockers=[blocker])


resolution = 3
bottom_left_coordinate = APIWorldCoordinates(lat=47.3695943521338, long=8.539376953124991)
top_right_coordinate = APIWorldCoordinates(lat=47.371034633497596, long=8.541363281249993)
map_height = 40
time_steps = 1000


def setup_map():
    area = Area(bottom_left_coordinate,
                top_right_coordinate,
                resolution)
    size = area.dimension
    map_dimensions = Coordinate4D(math.floor(size[0]),
                                  math.floor(map_height / area.resolution),
                                  math.floor(size[1]),
                                  time_steps)
    return EnvironmentGen(map_dimensions, [MapTile([15, 17161, 11475], area)], area)


def fcfs_simulation(_env: Environment):
    allocator = FCFSAllocator()
    payment_rule = FCFSPaymentRule()
    mechanism = Mechanism(allocator, payment_rule)
    owners = [
        WebPathOwner("0",
                     "Schnabeltier",
                     color_generator(),
                     [GridLocation(str(GridLocationType.RANDOM.value)),
                      GridLocation(str(GridLocationType.RANDOM.value))],
                     [random.randint(0, math.floor(allocation_period / 2)) for _ in range(nr_agents)],
                     FCFSPathBiddingStrategy(),
                     FCFSPathValueFunction(),
                     1,
                     2000,
                     1),
        WebSpaceOwner("1",
                      "Ghettotier",
                      color_generator(),
                      [GridLocation(str(GridLocationType.RANDOM.value)),
                       GridLocation(str(GridLocationType.RANDOM.value))],
                      [random.randint(0, allocation_period) for _ in range(nr_agents)],
                      space_dimensions,
                      FCFSSpaceBiddingStrategy(),
                      FCFSSpaceValueFunction())
    ]
    return Simulator(owners, mechanism, _env)


def priority_simulation(_env: Environment):
    allocator = PriorityAllocator()
    payment_rule = PriorityPaymentRule()
    mechanism = Mechanism(allocator, payment_rule)
    owners = [
        WebPathOwner("0",
                     "Schnabeltier",
                     color_generator(),
                     [GridLocation(str(GridLocationType.RANDOM.value)),
                      GridLocation(str(GridLocationType.RANDOM.value))],
                     [random.randint(0, math.floor(allocation_period / 2)) for _ in range(nr_agents)],
                     PriorityPathBiddingStrategy(),
                     PriorityPathValueFunction(),
                     1,
                     2000,
                     1,
                     {"priority": 1.0}),
        WebPathOwner("1",
                     "GhettoSalat",
                     color_generator(),
                     [GridLocation(str(GridLocationType.RANDOM.value)),
                      GridLocation(str(GridLocationType.RANDOM.value))],
                     [random.randint(0, math.floor(allocation_period / 2)) for _ in range(nr_agents)],
                     PriorityPathBiddingStrategy(),
                     PriorityPathValueFunction(),
                     1,
                     2000,
                     1,
                     {"priority": 0.1}),
        WebSpaceOwner("2",
                      "Ghettotier",
                      color_generator(),
                      [GridLocation(str(GridLocationType.RANDOM.value)),
                       GridLocation(str(GridLocationType.RANDOM.value))],
                      [random.randint(0, math.floor(allocation_period / 2)) for _ in range(nr_agents)],
                      space_dimensions,
                      PrioritySpaceBiddingStrategy(),
                      PrioritySpaceValueFunction(),
                      {"priority": 0.5}),
    ]
    return Simulator(owners, mechanism, _env)


def color_generator():
    while True:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        if r + g + b > 350:
            break
    return f"#{hex(r)[2:]:2}{hex(g)[2:]:2}{hex(b)[2:]:2}"


if __name__ == "__main__":
    pre_environment = setup_map()
    env = pre_environment.generate()
    simulatorAligator = priority_simulation(env)

    start = time.time_ns()
    while simulatorAligator.tick():
        pass

    sim_time = time.time_ns() - start

    print()
    print(f"SIM: {sim_time / 6e10:2.2f} min")
    print()

    tot_time = time.time_ns() - start
    print()
    print(f"TOTAL: {tot_time / 6e10:2.2f} min")
    sim_config = generate_config(simulatorAligator, pre_environment)
    statistics_start_time = time.time_ns()
    statistics = get_statistics_dict(simulatorAligator)
    statistics_end_time = time.time_ns()
    statistics_duration = statistics_end_time - statistics_start_time
    owner_map = {}
    for owner in simulatorAligator.owners:
        if isinstance(owner, WebSpaceOwner) or isinstance(owner, WebPathOwner):
            owner_map[owner.id] = JSONOwnerDescription(owner.color, owner.name).as_dict()
        else:
            owner_map[owner.id] = JSONOwnerDescription(owner.id, hex(hash(owner.id) % 0xFFFFFF)[2:].zfill(6)).as_dict()

    res = {"config": sim_config,
           "owner_map": owner_map,
           "simulation": get_simulation_dict(simulatorAligator),
           "statistics": statistics,
           "statistics_compute_time": statistics_duration,
           "simulation_compute_time": tot_time}
    get_statistics_dict(simulatorAligator)
    f = open("playground.json", "w")
    f.write(json.dumps(res))
    f.close()
