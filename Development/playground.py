import json
import random

from AAS import Simulator, Coordinate4D
from AAS.Blocker.StaticBlocker import StaticBlocker
from AAS.Coordinates.Coordinate3D import Coordinate3D
from AAS.Environment.Environment import Environment
from AAS.IO.JSONS import build_json
from AAS.Owners.GridLocation import GridLocation
from AAS.Owners.GridLocationType import GridLocationType
from AAS.Owners.PathOwners.ABOwner import ABOwner
from AAS.Owners.SpaceOwners.StationaryOwner import StationaryOwner
from API.API import APISimpleCoordinates
from API.Generator.MapTile import MapTile
from Demos.FCFS.Allocator.FCFSAllocator import FCFSAllocator

random.seed(3)


def setup_empty(t):
    dimensions = Coordinate4D(50, 20, 50, t)
    blocker = StaticBlocker(Coordinate3D(5, 0, 5), Coordinate3D(40, 15, 40))
    return Environment.init(dimensions, blocker=[blocker], allocation_period=20)


def setup_map(t):
    dimensions = Coordinate4D(831, 30, 831, t)
    map_tile = MapTile(
        [15, 17161, 11475],
        dimensions,
        APISimpleCoordinates(lat=47.376034633497596, long=8.536376953124991),
        APISimpleCoordinates(lat=47.3685943521338, long=8.547363281249993)
    )
    return Environment.init(dimensions, maptiles=[map_tile], allocation_period=20)


def simulate(env: Environment, t):
    allocator = FCFSAllocator()
    owners = [
        ABOwner("Schnabeltier",
                color_generator(),
                [GridLocation(str(GridLocationType.RANDOM.value)), GridLocation(str(GridLocationType.RANDOM.value))],
                [random.randint(0, 5) for _ in range(10)]),
        StationaryOwner("Ghettotier",
                        color_generator(),
                        [GridLocation(str(GridLocationType.RANDOM.value)),
                         GridLocation(str(GridLocationType.RANDOM.value))],
                        [random.randint(0, 5) for _ in range(10)])
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
    max_t = 100
    environment = setup_map(max_t)
    simulatorAligator = simulate(environment, max_t)

    res = build_json({"name": "test", "description": "Schnabeltier"}, simulatorAligator, 0)
    f = open("../test.json", "w")
    f.write(json.dumps(res))
    f.close()
