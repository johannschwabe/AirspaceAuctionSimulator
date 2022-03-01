import random

from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import Coordinate
from Simulator.helpers.History import History
from Simulator import Simulator, Statistics, Environment
from owners.ABAOwner import ABAOwner
from owners.ABOwner import ABOwner
from owners.BlockerOwner import BlockerOwner

dimensions = Coordinate(10, 10, 1)
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
owners = [ABAOwner([1]), ABOwner([1]), BlockerOwner([1, 1, 1, 1, 1, 1])]

history = History()
simulator = Simulator(owners, allocator, environment, history)
simulator.setup()

while simulator.time_step < 50:
    environment.visualize(simulator.time_step)
    simulator.tick()
    pass

stats = Statistics(simulator)
stats.non_colliding_values()
print("done")
