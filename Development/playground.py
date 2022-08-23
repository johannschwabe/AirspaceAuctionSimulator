import json
import random

from Demos.FCFS.Allocator.FCFSAllocator import FCFSAllocator
from Demos.FCFS.Owners.FCFSPathOwner import FCFSPathOwner
from Demos.FCFS.Owners.FCFSSpaceOwner import FCFSSpaceOwner
from Demos.Priority.Allocator.PriorityAllocator import PriorityAllocator
from Demos.Priority.Owners.PriorityPathOwner import PriorityPathOwner
from Demos.Priority.Owners.PrioritySpaceOwner import PrioritySpaceOwner
from Simulator import Simulator, Coordinate4D
from Simulator.Blocker.StaticBlocker import StaticBlocker
from Simulator.Coordinates.Coordinate3D import Coordinate3D
from Simulator.Environment.Environment import Environment
from Simulator.IO.JSONS import build_json
from Simulator.Owners.Location.GridLocation import GridLocation
from Simulator.Owners.Location.GridLocationType import GridLocationType

random.seed(3)


def setup_empty(t):
    dimensions = Coordinate4D(50, 20, 50, t)
    blocker = StaticBlocker(Coordinate3D(5, 0, 5), Coordinate3D(40, 15, 40))
    return Environment(dimensions, blockers=[blocker], allocation_period=20)


def simulateFCFS(env: Environment, t):
    allocator = FCFSAllocator()
    owners = [
        FCFSPathOwner(0,
                      "Schnabeltier",
                      color_generator(),
                      [GridLocation(str(GridLocationType.RANDOM.value)),
                       GridLocation(str(GridLocationType.RANDOM.value))],
                      [random.randint(0, 5) for _ in range(10)]),
        FCFSSpaceOwner(1,
                       "Ghettotier",
                       color_generator(),
                       [GridLocation(str(GridLocationType.RANDOM.value)),
                        GridLocation(str(GridLocationType.RANDOM.value))],
                       [random.randint(0, 5) for _ in range(10)],
                       Coordinate4D(25, 25, 25, 25))
    ]
    simulator = Simulator(owners, allocator, env)
    while simulator.time_step < t:
        simulator.tick()

    return simulator


def simulatePriority(env: Environment, t):
    allocator = PriorityAllocator()
    owners = [
        PriorityPathOwner(0,
                          "Schnabeltier",
                          color_generator(),
                          [GridLocation(str(GridLocationType.RANDOM.value)),
                           GridLocation(str(GridLocationType.RANDOM.value))],
                          [random.randint(0, 5) for _ in range(10)],
                          priority=0.5),
        PrioritySpaceOwner(1,
                           "Ghettotier",
                           color_generator(),
                           [GridLocation(str(GridLocationType.RANDOM.value)),
                            GridLocation(str(GridLocationType.RANDOM.value))],
                           [random.randint(0, 5) for _ in range(10)],
                           Coordinate4D(25, 25, 25, 25),
                           priority=1.0)
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
    environment = setup_empty(max_t)
    simulatorAligator = simulatePriority(environment, max_t)

    res = build_json(simulatorAligator, 0)
    res["config"] = {"name": "test", "map": {"tiles": []}, "dimension": environment.dimension.to_dict(), "owners": []}
    f = open("test.json", "w")
    f.write(json.dumps(res))
    f.close()
