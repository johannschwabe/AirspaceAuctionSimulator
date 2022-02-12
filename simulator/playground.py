import random

from simulator.coordinates import Coordinate
from simulator.owners.OwnerA import OwnerA
from simulator.allocators.AllocatorA import AllocatorA
from simulator.environments.EnvironmentA import EnvironmentA
from simulator.helpers.History import History
from Simulator import Simulator
from simulator.statistics.Statistics import Statistics

random.seed(2)

dim = Coordinate(10,10,1)
envi = EnvironmentA(dim)
alloci = AllocatorA(envi)
owners = []
for _ in range(3):
    owners.append(OwnerA(envi))

histi = History()
stats = Statistics()
simi = Simulator(owners, alloci, envi, histi, [], stats)
simi.setup()
envi.visualize(0)
while simi.tick():
    pass

print("done")
