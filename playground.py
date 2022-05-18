import random
from time import time_ns

from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator.Environment import Environment
from Simulator import Simulator, Tick, Statistics
from Simulator.IO.JSONS import build_json
from Simulator.History import History
from Simulator.Owner.ABOwner import ABOwner
from cbs.CBSAllocator import CBS
from Simulator.Owner.CBSTestOwner import CBSTestOwner

dimensions = TimeCoordinate(50, 50, 50, Tick(30))
random.seed(2)
environment = Environment(dimensions, [])
# allocator = FCFSAllocator()
allocator = CBS()
owners = [ABOwner("Schnabeltier", "red", [0]*13)]

history = History(dimensions, allocator, environment, owners)
simulator = Simulator(owners, allocator, environment, history)
t0 = time_ns()
while simulator.time_step < dimensions.t:
    print(simulator.time_step)
    # simulator.environment.visualize(simulator.time_step)
    simulator.tick()
print(f"Total: {(time_ns() - t0)/1e9}")

# res = build_json(simulator, "test", "Schnabeltier")
stats = Statistics(simulator)
close_passings = stats.close_passings()
total_wellfare = stats.total_agents_welfare()
print(close_passings)
print(total_wellfare)
print("done")
