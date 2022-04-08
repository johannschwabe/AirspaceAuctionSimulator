import random
from time import time_ns

from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator.Environment import Environment
from Simulator import Simulator, Statistics, Tick
from Simulator.Owner.ABAOwner import ABAOwner
from Simulator.Owner.ABCOwner import ABCOwner
from Simulator.History import History
from Simulator.Owner.ABOwner import ABOwner
from Simulator.Owner.StationaryOwner import StationaryOwner

dimensions = TimeCoordinate(1000, 1000, 100, Tick(100))
random.seed(2)
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
owners = [ABOwner(list(range(10))), ABAOwner(list(range(10))), ABCOwner(list(range(10))), StationaryOwner(list(range(10)))]

history = History(dimensions, allocator, environment, owners)
simulator = Simulator(owners, allocator, environment, history)
t0 = time_ns()
while simulator.time_step < dimensions.t:
    print(simulator.time_step)
    simulator.tick()
print(f"Total: {(time_ns() - t0)/1e9}")
stats = Statistics(simulator)
stats.non_colliding_values()
# cols, nfc, nfi, ffc, ffi = stats.close_passings()
stats.average_owners_welfare()
stats.average_agents_welfare()
print("done")
