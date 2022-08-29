import json
import math
import random
import time

from API import Area, APIWorldCoordinates
from API.Generator.EnvironmentGen import EnvironmentGen
from API.Generator.MapTile import MapTile
from Demos.FCFS import FCFSAllocator, FCFSPathOwner, FCFSSpaceOwner, FCFSPaymentRule
from Demos.Priority import PriorityAllocator, PriorityPathOwner, PrioritySpaceOwner, PriorityPaymentRule
from Simulator import \
    Simulator, \
    Coordinate4D, \
    StaticBlocker, \
    Coordinate3D, \
    Environment, \
    GridLocation, \
    GridLocationType, \
    build_json, \
    Mechanism

random.seed(4)
dimensions = Coordinate4D(40, 40, 40, 1000)
allocation_period = 100
space_dimensions = Coordinate4D(7, 7, 7, 10)
nr_agents = 10


def setup_empty():
    blocker = StaticBlocker(Coordinate3D(10, 0, 10), Coordinate3D(20, 20, 20))
    return Environment(dimensions, blockers=[blocker], allocation_period=allocation_period)


resolution = 2
bottom_left_coordinate = APIWorldCoordinates(lat=47.3685943521338, long=8.536376953124991)
top_right_coordinate = APIWorldCoordinates(lat=47.376034633497596, long=8.547363281249993)
map_height = 40
time_steps = 1000


def setup_map():
    random.seed(0)
    area = Area(bottom_left_coordinate,
                top_right_coordinate,
                resolution)
    size = area.dimension
    map_dimensions = Coordinate4D(math.floor(size[0]),
                                  math.floor(map_height / area.resolution),
                                  math.floor(size[1]),
                                  time_steps)
    print(dimensions)
    return EnvironmentGen(map_dimensions, [MapTile([15, 17161, 11475], area)]).generate()


def fcfsSimulation(env: Environment):
    allocator = FCFSAllocator()
    payment_rule = FCFSPaymentRule()
    mechanism = Mechanism(allocator, payment_rule)
    owners = [
        FCFSPathOwner("0",
                      "Schnabeltier",
                      color_generator(),
                      [GridLocation(str(GridLocationType.RANDOM.value)),
                       GridLocation(str(GridLocationType.RANDOM.value))],
                      [random.randint(0, math.floor(allocation_period / 2)) for _ in range(nr_agents)]),
        FCFSSpaceOwner("1",
                       "Ghettotier",
                       color_generator(),
                       [GridLocation(str(GridLocationType.RANDOM.value)),
                        GridLocation(str(GridLocationType.RANDOM.value))],
                       [random.randint(0, allocation_period) for _ in range(nr_agents)],
                       space_dimensions)
    ]
    return Simulator(owners, mechanism, env)


def prioritySimulation(env: Environment):
    allocator = PriorityAllocator()
    payment_rule = PriorityPaymentRule()
    mechanism = Mechanism(allocator, payment_rule)
    owners = [
        PriorityPathOwner("0",
                          "Schnabeltier",
                          color_generator(),
                          [GridLocation(str(GridLocationType.RANDOM.value)),
                           GridLocation(str(GridLocationType.RANDOM.value))],
                          [random.randint(0, math.floor(allocation_period / 2)) for _ in range(nr_agents)],
                          priority=1.0),
        PriorityPathOwner("1",
                          "GhettoSalat",
                          color_generator(),
                          [GridLocation(str(GridLocationType.RANDOM.value)),
                           GridLocation(str(GridLocationType.RANDOM.value))],
                          [random.randint(0, math.floor(allocation_period / 2)) for _ in range(nr_agents)],
                          priority=0.1),
        PrioritySpaceOwner("2",
                           "Ghettotier",
                           color_generator(),
                           [GridLocation(str(GridLocationType.RANDOM.value)),
                            GridLocation(str(GridLocationType.RANDOM.value))],
                           [random.randint(0, allocation_period) for _ in range(nr_agents)],
                           space_dimensions,
                           priority=0.5)
    ]
    return Simulator(owners, mechanism, env)


def color_generator():
    while True:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        if r + g + b > 350:
            break
    return f"#{hex(r)[2:]:02}{hex(g)[2:]:02}{hex(b)[2:]:02}"


if __name__ == "__main__":
    environment = setup_map()
    simulatorAligator = prioritySimulation(environment)

    start = time.time_ns()
    while simulatorAligator.tick():
        pass

    sim_time = time.time_ns() - start

    print()
    print(f"SIM: {sim_time / 6e10:2.2f} min")
    print()

    res = build_json(simulatorAligator, sim_time)
    res["config"] = {"name": "test",
                     "map": {"tiles": []},
                     "dimension": environment.dimension.to_dict(),
                     "owners": []}

    tot_time = time.time_ns() - start
    print()
    print(f"TOTAL: {tot_time / 6e10:2.2f} min")

    f = open("playground.json", "w")
    f.write(json.dumps(res))
    f.close()
