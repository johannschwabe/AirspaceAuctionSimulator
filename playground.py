import json
import random
from time import time_ns

from API import SimpleCoordinateType
from BiddingAllocator.BiddingABOwner import BiddingABOwner
from BiddingAllocator.BiddingAllocator import BiddingAllocator
from BiddingAllocator.BiddingStationaryOwner import BiddingStationaryOwner
from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import Coordinate4D
from Simulator.Environment import Environment
from Simulator import Simulator
from Simulator.Generator.MapTile import MapTile
from Simulator.IO.JSONS import build_json
from Simulator.History import History


def setup_empty():
    dimensions = Coordinate4D(50, 20, 50, 20)
    random.seed(3)
    environment = Environment(dimensions, [], [])
    environment.init_blocker_tree()
    allocator = BiddingAllocator()
    owners = []

    for i in range(10):
        # owners.append(BiddingABOwner("Schnabeltier" + str(i),
        #                              color_generator(),
        #                              [random.randint(0, 5) for _ in range(10)],
        #                              random.uniform(0,1)
        #                              ))
        owners.append(BiddingStationaryOwner(
            "GhettoTier",
            color_generator(),
            [random.randint(0, 5) for _ in range(10)],
            1,
            Coordinate4D(5, 5, 5, 3),
            random.uniform(0, 1)
        ))

    history = History(dimensions, allocator, environment, owners)
    SimulaterAligator = Simulator(owners, allocator, environment, history)
    t0 = time_ns()
    while SimulaterAligator.time_step < dimensions.t:
        # print(simulator.time_step)
        SimulaterAligator.tick()
        # SimulaterAligator.environment.visualize(SimulaterAligator.time_step)
    print(f"Total: {(time_ns() - t0) / 1e9}")

    res = build_json(SimulaterAligator, "test", "Schnabeltier")
    f = open("test.json", "w")
    f.write(json.dumps(res))
    f.close()


def setup_map():
    dimensions = Coordinate4D(831, 30, 831, 20)
    random.seed(3)
    environment = Environment(dimensions, [], [MapTile(
        [15, 17161, 11475],
        dimensions,
        SimpleCoordinateType(lat=47.376034633497596, long=8.536376953124991),
        SimpleCoordinateType(lat=47.3685943521338, long=8.547363281249993)
    )])
    environment.init_blocker_tree()
    allocator = BiddingAllocator()
    # allocator = FCFSAllocator()
    owners = []
    # owners.append(TestOwner("test", "#6EFF40", [
    #     Coordinate4D(457, 0, 493, Tick(1)),
    #     Coordinate4D(431, 21, 519, Tick(21))
    # ]))
    # for i in range(4):
    #     owners.append(ABCOwner("Schnabeltier"+ str(i), "#00C362", [random.randint(0,5) for _ in range(10)]))
    for i in range(30):
        owners.append(BiddingABOwner("Schnabeltier" + str(i),
                                     color_generator(),
                                     [random.randint(0, 5) for _ in range(10)],
                                     random.uniform(0,1)
                                     ))
    # owners = [BiddingABOwner("Schnabeltier", "#00C362", [1, 1, 1, 2], 0.5),
    #           BiddingABOwner("Schnabeltier", "#DE4242", [1, 1, 3, 3, 3], 0.7)]

    history = History(dimensions, allocator, environment, owners)
    SimulaterAligator = Simulator(owners, allocator, environment, history)
    t0 = time_ns()
    while SimulaterAligator.time_step < dimensions.t:
        # print(simulator.time_step)
        SimulaterAligator.tick()
        # SimulaterAligator.environment.visualize(SimulaterAligator.time_step)
    print(f"Total: {(time_ns() - t0) / 1e9}")

    res = build_json(SimulaterAligator, "test", "Schnabeltier")
    f = open("test.json", "w")
    f.write(json.dumps(res))
    f.close()
    # print(res)
    # print("agents: ", res['statistics']['total_number_of_agents'])
    # print("cols: ", res['statistics']['total_number_of_collisions'])
    # print("wf: ", res['statistics']['total_achieved_welfare'])
    print("done")


def color_generator():
    while True:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        if r + g + b > 350:
            break
    return f"#{hex(r)[2:]:02}{hex(g)[2:]:02}{hex(b)[2:]:02}"



if __name__ == "__main__":
    setup_empty()
