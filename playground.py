import random

from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import Coordinate
from Simulator.History2.History import History2
from Simulator.helpers.History import History
from Simulator import Simulator, Statistics, Environment
from owners.ABAOwner import ABAOwner
from owners.ABCOwner import ABCOwner
from owners.ABOwner import ABOwner
from owners.BlockerOwner import BlockerOwner

dimensions = Coordinate(20, 20, 1)
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
owners = [ABAOwner([0, 0]), ABOwner([0, 0]), BlockerOwner([1, 1, 1, 1, 1]), ABCOwner([0, 0, 0, 0, 0])]

history = History2(dimensions,allocator, environment)
simulator = Simulator(owners, allocator, environment, history)
simulator.setup()

while simulator.time_step < 50:
    environment.visualize(simulator.time_step)
    simulator.tick()
    pass

stats = Statistics(simulator)
stats.non_colliding_values()
print("done")
