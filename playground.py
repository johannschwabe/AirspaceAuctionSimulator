import random

from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import Coordinate
from Simulator.Environment.Environment import Environment
from Simulator.History2.History import History2
from Simulator import Simulator, Statistics
from owners.ABAOwner import ABAOwner
from owners.ABCOwner import ABCOwner
from owners.ABOwner import ABOwner
from owners.BlockerOwner import BlockerOwner

dimensions = Coordinate(10, 10, 1)
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
owners = [ABOwner([0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 3, 4, 5, 10, 20, 20])]

history = History2(dimensions,allocator, environment)
history.set_owners(owners)
simulator = Simulator(owners, allocator, environment, history)
simulator.setup()

while simulator.time_step < 50:
    environment.visualize(simulator.time_step)
    simulator.tick()
    pass

stats = Statistics(simulator)
stats.non_colliding_values()
stats.close_passings()
stats.average_owners_welfare()
stats.average_agents_welfare()
print("done")
