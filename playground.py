import random
from time import time_ns

from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator.Environment import Environment
from Simulator import Simulator, Tick
from Simulator.Generator.BlockerGen import BlockerGen
from Simulator.IO.JSONS import build_json
from Simulator.History import History
from Simulator.Owner.ABAOwner import ABAOwner
from Simulator.Owner.ABCOwner import ABCOwner
from Simulator.Owner.ABOwner import ABOwner
from Simulator.Owner.StationaryOwner import StationaryOwner

dimensions = TimeCoordinate(20, 2, 20, Tick(20))
random.seed(2)
environment = Environment(dimensions)
blocker_gen = BlockerGen(dimensions)
environment.set_blockers(blocker_gen.generate(20))
allocator = FCFSAllocator()
owners = [
    ABOwner("Schnabeltier", "red", [1, 1, 1, 1, 1]),
    ABCOwner("Schnabeltier", "red", [1, 1, 1, 1, 1]),
    ABAOwner("Schnabeltier", "red", [1, 1, 1, 1, 1]),
    StationaryOwner("Schnabeltier", "red", [1, 1, 1, 1, 1]),
]

history = History(dimensions, allocator, environment, owners)
simulator = Simulator(owners, allocator, environment, history)
t0 = time_ns()
while simulator.time_step < dimensions.t:
    print(simulator.time_step)
    simulator.environment.visualize(simulator.time_step)
    simulator.tick()
print(f"Total: {(time_ns() - t0) / 1e9}")

res = build_json(simulator, "test", "Schnabeltier")
print("done")
