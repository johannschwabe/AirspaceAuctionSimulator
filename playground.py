import random
from time import time_ns

from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator.Environment import Environment
from Simulator import Simulator, Statistics, Tick
from Simulator.Owner.ABAOwner import ABAOwner
from Simulator.Owner.ABCOwner import ABCOwner
from Simulator.History2 import History2
from Simulator.Owner.ABOwner import ABOwner
from Simulator.Owner.StationaryOwner import StationaryOwner

dimensions = TimeCoordinate(10, 10, 1, Tick(100))
random.seed(2)
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
owners = [ABOwner([1,1,1,1,1])]

history = History2(dimensions, allocator, environment, owners)
simulator = Simulator(owners, allocator, environment, history)
t0 = time_ns()
while simulator.time_step < dimensions.t:
    print(simulator.time_step)
    simulator.environment.visualize(simulator.time_step)
    simulator.tick()
print(f"Total: {(time_ns() - t0)/1e9}")
stats = Statistics(simulator)
print(stats.close_passings())
stats.non_colliding_values()
stats.average_owners_welfare()
stats.average_agents_welfare()
print("done")
