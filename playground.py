import json
import random

from API import APISimpleCoordinate
from FCFSAllocator.FCFSAllocator import FCFSAllocator
from Simulator.Coordinate import Coordinate4D, Coordinate3D
from Simulator.Environment import Environment
from Simulator import Simulator, Blocker
from Simulator.Generator.MapTile import MapTile
from Simulator.IO.JSONS import build_json
from Simulator.Owner import PathStop, StopType
from Simulator.Owner.PathOwners.ABOwner import ABOwner
from Simulator.Owner.SpaceOwners.StationaryOwner import StationaryOwner


random.seed(3)


def setup_empty(t):
    dimensions = Coordinate4D(50, 20, 50, t)
    blocker = Blocker([Coordinate4D(5, 0, 5, t) for t in range(1000)], Coordinate3D(40, 15, 40))
    return Environment.init(dimensions, blocker=[blocker])


def setup_map(t):
    dimensions = Coordinate4D(831, 30, 831, t)
    map_tile = MapTile(
        [15, 17161, 11475],
        dimensions,
        APISimpleCoordinate(lat=47.376034633497596, long=8.536376953124991),
        APISimpleCoordinate(lat=47.3685943521338, long=8.547363281249993)
    )
    return Environment.init(dimensions, maptiles=[map_tile])


def simulate(env: Environment, t):
    allocator = FCFSAllocator()
    owners = [
        ABOwner("Schnabeltier",
                color_generator(),
                [PathStop(StopType.RANDOM), PathStop(StopType.RANDOM)],
                [random.randint(0, 5) for _ in range(100)]),
        StationaryOwner("GhettoTier",
                        color_generator(),
                        [random.randint(0, 5) for _ in range(10)],
                        1,
                        Coordinate4D(5, 5, 5, 3)),
    ]
    simulator = Simulator(owners, allocator, env)
    while simulator.time_step < t:
        simulator.tick()

    return simulator


def color_generator():
    while True:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        if r + g + b > 350:
            break
    return f"#{hex(r)[2:]:02}{hex(g)[2:]:02}{hex(b)[2:]:02}"


if __name__ == "__main__":
    max_t = 20
    environment = setup_empty(max_t)
    simulatorAligator = simulate(environment, max_t)

    res = build_json(simulatorAligator, "test", "Schnabeltier")
    f = open("test.json", "w")
    f.write(json.dumps(res))
    f.close()
