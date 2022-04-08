import random
from time import time_ns

from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator.Environment import Environment
from Simulator import Simulator, Statistics, Tick
from Simulator.History import History
from owners.ABAOwner import ABAOwner
from owners.ABCOwner import ABCOwner
from Simulator.History2 import History2
from owners.ABOwner import ABOwner
from owners.StationaryOwner import StationaryOwner

dimensions = TimeCoordinate(100, 100, 10, Tick(1000))
random.seed(2)
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
# owners = [ABOwner([i for i in range(10)]), ABAOwner([i for i in range(10)]), ABCOwner([i for i in range(10)]), StationaryOwner([i for i in range(10)])]
owners = [ABCOwner([i for i in range(10)])]

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
