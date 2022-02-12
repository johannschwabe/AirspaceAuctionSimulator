import random

from Simulator.Coordinate import Coordinate
from Simulator.Owner.OwnerA import OwnerA
from Simulator.Allocator.AllocatorA import AllocatorA
from Simulator.Environment.EnvironmentA import EnvironmentA
from Simulator.helpers.History import History
from Simulator import Simulator, Statistics

random.seed(2)

dim = Coordinate(10, 10, 1)
envi = EnvironmentA(dim)
alloci = AllocatorA(envi)
owners = []
for _ in range(3):
    owners.append(OwnerA(envi))

histi = History()
stats = Statistics()
simi = Simulator(owners, alloci, envi, histi, [])
simi.setup()
envi.visualize(0)
while simi.tick():
    pass

print("done")
