from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator.Environment import Environment
from Simulator import Simulator, Statistics, Tick
from Simulator.History import History
from Simulator.History2 import History2
from owners.ABOwner import ABOwner
from time import time_ns
import random
random.seed(2)
dimensions = TimeCoordinate(10, 10, 1, Tick(60))
TimeCoordinate.dim = dimensions
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
owners = [ABOwner([0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 3, 4, 5, 10, 20, 20])]

history = History2(dimensions, allocator, environment, owners)
simulator = Simulator(owners, allocator, environment, history)
t0 = time_ns()
while simulator.time_step < dimensions.t:
    # environment.visualize(simulator.time_step)
    simulator.tick()
print(f"Total: {(time_ns() - t0)/1e9}")
history = History("bls", "blub", simulator)
stats = Statistics(simulator)
stats.non_colliding_values()
cols, nfc, nfi, ffc, ffi = stats.close_passings()
stats.average_owners_welfare()
stats.average_agents_welfare()
print("done")
