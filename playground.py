import random
from time import time_ns

from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator.Environment import Environment
from Simulator import Simulator, Tick
from Simulator.IO.JSONS import build_json
from Simulator.History import History
from Simulator.Owner.ABOwner import ABOwner

dimensions = TimeCoordinate(10, 10, 1, Tick(100))
random.seed(2)
environment = Environment(dimensions, [],[])
environment.set_blockers([])
allocator = FCFSAllocator()
owners = [ABOwner(f"Schnabeltier{i}", "red", [1, 1, 1, 1, 1]) for i in range(3)]

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
