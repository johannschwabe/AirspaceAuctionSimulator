import random

from Simulator.Coordinate import Coordinate
from Simulator.helpers.History import History
from Simulator import Simulator, Statistics, Environment
from owners.HobbyPilotOwner import HobbyPilotOwner
from owners.JohannOwner import JohannOwner
from owners.ThomasOwner import ThomasOwner
from allocators.FCFSAllocator import FCFSAllocator

random.seed(2)

dimensions = Coordinate(10, 10, 1)
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
# allocator = JohannAllocator()
owners = [ThomasOwner([1, 2, 2, 5, 6, 10, 15]),
          JohannOwner(),
          HobbyPilotOwner(Coordinate(2, 2, 0), Coordinate(4, 4, 0), 10, 20, 2)]

history = History()
simulator = Simulator(50, owners, allocator, environment, history)
simulator.setup()

while simulator.tick():
    environment.visualize(simulator.time_step)

stats = Statistics(simulator)
stats.non_colliding_values()
print("done")
