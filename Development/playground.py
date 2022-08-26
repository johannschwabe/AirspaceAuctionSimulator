import json
import math
import random

from Mechanisms.FCFS import FCFSAllocator, FCFSPathOwner, FCFSSpaceOwner
from Mechanisms.FCFS.PaymentRule.FCFSPaymentRule import FCFSPaymentRule
from Mechanisms.Priority import PriorityAllocator, PriorityPathOwner, PrioritySpaceOwner
from Mechanisms.Priority.PaymentRule.PriorityPaymentRule import PriorityPaymentRule
from Simulator import \
    Simulator, \
    Coordinate4D, \
    StaticBlocker, \
    Coordinate3D, \
    Environment, \
    GridLocation, \
    GridLocationType, \
    build_json
from Simulator.Mechanism.Mechanism import Mechanism

random.seed(3)
dimensions = Coordinate4D(40, 40, 40, 1000)
allocation_period = 40
space_dimensions = Coordinate4D(10, 10, 10, 20)
nr_agents = 10


def setup_empty():
    blocker = StaticBlocker(Coordinate3D(10, 0, 10), Coordinate3D(20, 20, 20))
    return Environment(dimensions, blockers=[blocker], allocation_period=allocation_period)


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
                          priority=0.5),
        PrioritySpaceOwner("1",
                           "Ghettotier",
                           color_generator(),
                           [GridLocation(str(GridLocationType.RANDOM.value)),
                            GridLocation(str(GridLocationType.RANDOM.value))],
                           [random.randint(0, allocation_period) for _ in range(nr_agents)],
                           space_dimensions,
                           priority=1.0)
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
    environment = setup_empty()
    simulatorAligator = prioritySimulation(environment)

    while simulatorAligator.tick():
        pass

    res = build_json(simulatorAligator, 0)
    res["config"] = {"name": "test", "map": {"tiles": []}, "dimension": environment.dimension.to_dict(), "owners": []}
    f = open("Development/playground.json", "w")
    f.write(json.dumps(res))
    f.close()
