import random

from Simulator.Coordinate import Coordinate
from Simulator.Owner.OwnerA import OwnerA
from Simulator.Allocator.AllocatorA import AllocatorA
from Simulator.Environment.EnvironmentA import EnvironmentA
from Simulator.helpers.History import History
from Simulator import Simulator, Statistics

random.seed(2)

dimensions = Coordinate(10, 10, 1)
environment = EnvironmentA(dimensions)
allocator = AllocatorA()
owners = []
for _ in range(3):
    owners.append(OwnerA())

history = History()
simulator = Simulator(owners, allocator, environment, history)
simulator.setup()

while simulator.time_step < 100:
    environment.visualize(simulator.time_step)
    simulator.tick()
    pass

stats = Statistics(simulator)
stats.non_colliding_values()
print("done")
