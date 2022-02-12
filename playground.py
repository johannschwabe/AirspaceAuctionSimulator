import random

from Simulator.Coordinate import Coordinate
from Simulator.helpers.History import History
from Simulator import Simulator, Statistics, Environment
from allocators.JohannAllocator import JohannAllocator
from owners.JohannOwner import JohannOwner
from owners.ThomasOwner import ThomasOwner
from allocators.FCFSAllocator import FCFSAllocator

random.seed(2)

dimensions = Coordinate(10, 10, 1)
environment = Environment(dimensions, [])
# allocator = FCFSAllocator()
allocator = JohannAllocator()
owners = [ThomasOwner([1, 2, 2, 5, 6, 10, 15]), JohannOwner()]

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
