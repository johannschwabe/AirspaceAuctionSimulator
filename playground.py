import random

from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator import Simulator, Statistics, Environment, Tick
from Simulator.History import History
from owners.ABAOwner import ABAOwner
from owners.ABCOwner import ABCOwner
from owners.ABOwner import ABOwner
from owners.BlockerOwner import BlockerOwner

dimensions = TimeCoordinate(20, 20, 1, Tick(50))
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
owners = [ABAOwner([0, 0]), ABOwner([0, 0]), BlockerOwner([1, 1, 1, 1, 1]), ABCOwner([0, 0, 0, 0, 0])]

simulator = Simulator(owners, allocator, environment)

while simulator.time_step < dimensions.t:
    environment.visualize(simulator.time_step)
    simulator.tick()

history = History("bls", "blub", simulator)
stats = Statistics(history, allocator)
stats.non_colliding_values()
print("done")
