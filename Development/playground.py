import math
import random
import time

from API import Area, APIWorldCoordinates, EnvironmentGen, MapTile, WebPathOwner, \
    WebSpaceOwner, generate_config
from API.Owners.WebOwnerMixin import WebOwnerMixin
from API.Types import APISubselection
from Demos.FCFS import FCFSAllocator, FCFSPaymentRule, FCFSPathBiddingStrategy, FCFSSpaceBiddingStrategy, \
    FCFSPathValueFunction, FCFSSpaceValueFunction
from Demos.Priority import PriorityAllocator, PriorityPaymentRule, PriorityPathBiddingStrategy, \
    PriorityPathValueFunction, PrioritySpaceBiddingStrategy, PrioritySpaceValueFunction
from Simulator import Simulator, Coordinate4D, StaticBlocker, Coordinate3D, Environment, GridLocation, \
    GridLocationType, Mechanism
from Simulator.IO.JSONS import get_simulation_dict, JSONOwnerDescription
from Simulator.IO.Statistics import get_statistics_dict

random.seed(4)
dimensions = Coordinate4D(40, 40, 40, 1000)
allocation_period = 100
space_dimensions = Coordinate4D(7, 7, 7, 10)
nr_agents = 30


def setup_empty():
    blocker = StaticBlocker(Coordinate3D(10, 0, 10), Coordinate3D(20, 20, 20))
    return Environment(dimensions, blockers=[blocker], allocation_period=allocation_period)


resolution = 3
bottom_left_coordinate = APIWorldCoordinates(lat=47.3695943521338, long=8.539376953124991)
top_right_coordinate = APIWorldCoordinates(lat=47.371034633497596, long=8.541363281249993)
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
    return EnvironmentGen(map_dimensions, [MapTile([15, 17161, 11475], area)], area, 50, 10)


def fcfs_simulation(env: Environment):
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
    return Simulator(owners, mechanism, env)


def priority_simulation(env: Environment):
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
    sim_config = generate_config(simulatorAligator,
                                 APISubselection(bottomLeft=bottom_left_coordinate, topRight=top_right_coordinate),
                                 pre_environment.maptiles)
    statistics_start_time = time.time_ns()
    statistics = get_statistics_dict(simulatorAligator)
    statistics_end_time = time.time_ns()
    statistics_duration = statistics_end_time - statistics_start_time
    owner_map = {
        owner.id: JSONOwnerDescription(owner.color, owner.name).as_dict() if isinstance(owner, WebOwnerMixin)
        else JSONOwnerDescription(
            owner.id,
            hex(hash(owner.id) % 0xFFFFFF)[2:].zfill(6)).as_dict()
        for owner in simulatorAligator.owners}
    res = {"config": sim_config,
           "owner_map": owner_map,
           "simulation": get_simulation_dict(simulatorAligator),
           "statistics": statistics,
           "statistics_compute_time": statistics_duration,
           "simulation_compute_time": tot_time}
    get_statistics_dict(simulatorAligator)
    # f = open("playground.json", "w")
    # f.write(json.dumps(res))
    # f.close()
