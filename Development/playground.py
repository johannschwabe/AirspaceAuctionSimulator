import json
import math
import random

from Demos import PriorityAllocator, PrioritySpaceOwner, PriorityPathOwner
from Mechanisms import FCFSAllocator, FCFSPathOwner, FCFSSpaceOwner
from Simulator import \
    Simulator, \
    Coordinate4D, \
    StaticBlocker, \
    Coordinate3D, \
    Environment, \
    GridLocation, \
    GridLocationType, \
    build_json

random.seed(3)


def setup_empty(t):
    dimensions = Coordinate4D(40, 40, 40, t)
    blocker = StaticBlocker(Coordinate3D(10, 0, 10), Coordinate3D(20, 20, 20))
    return Environment(dimensions, blockers=[blocker], allocation_period=math.floor(t / 10))


def simulateFCFS(env: Environment, t):
    allocator = FCFSAllocator()
    owners = [
        FCFSPathOwner("owner-0",
                      "Schnabeltier",
                      color_generator(),
                      [GridLocation(str(GridLocationType.RANDOM.value)),
                       GridLocation(str(GridLocationType.RANDOM.value))],
                      [random.randint(0, 5) for _ in range(10)]),
        FCFSSpaceOwner("owner-1",
                       "Ghettotier",
                       color_generator(),
                       [GridLocation(str(GridLocationType.RANDOM.value)),
                        GridLocation(str(GridLocationType.RANDOM.value))],
                       [random.randint(0, 10) for _ in range(10)],
                       Coordinate4D(10, 10, 10, 10))
    ]
    simulator = Simulator(owners, allocator, env)
    while simulator.time_step < t:
        simulator.tick()

    return simulator


def simulatePriority(env: Environment, t):
    allocator = PriorityAllocator()
    owners = [
        PriorityPathOwner("owner-0",
                          "Schnabeltier",
                          color_generator(),
                          [GridLocation(str(GridLocationType.RANDOM.value)),
                           GridLocation(str(GridLocationType.RANDOM.value))],
                          [random.randint(0, 5) for _ in range(10)],
                          priority=0.5),
        PrioritySpaceOwner("owner-1",
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
    max_t = 1000
    environment = setup_empty(max_t)
    simulatorAligator = simulateFCFS(environment, max_t)

    res = build_json(simulatorAligator, 0)
    res["config"] = {"name": "test", "map": {"tiles": []}, "dimension": environment.dimension.to_dict(), "owners": []}
    f = open("Development/playground.json", "w")
    f.write(json.dumps(res))
    f.close()
