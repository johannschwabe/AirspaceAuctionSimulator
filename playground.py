import random

from Simulator.Coordinate import Coordinate
from Simulator.helpers.History import History
from Simulator import Simulator, Statistics, Environment

from owners.ThomasOwner import OwnerB
from allocators.FCFSAllocator import FCFSAllocator

random.seed(2)

dimensions = Coordinate(10, 10, 1)
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
owners = [OwnerB([1, 2, 2, 5, 6, 10, 15])]

history = History()
simulator = Simulator(owners, allocator, environment, history)
simulator.setup()

while simulator.time_step < 30:
    environment.visualize(simulator.time_step)
    simulator.tick()
    pass

stats = Statistics(simulator)
stats.non_colliding_values()
print("done")
