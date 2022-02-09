from simulator.owners.OwnerA import OwnerA
from simulator.allocators.AllocatorA import AllocatorA
from simulator.environments.EnvironmentA import EnvironmentA
from simulator.helpers.History import History
from Simulator import Simulator
from simulator.coordinates.Coordinates import Coordinates
from simulator.statistics.Statistics import Statistics

dim = Coordinates(10,10,1)
envi = EnvironmentA(dim)
alloci = AllocatorA(envi)
owners = [OwnerA(envi), OwnerA(envi), OwnerA(envi), OwnerA(envi), OwnerA(envi), OwnerA(envi)]

histi = History()
stats = Statistics()
simi = Simulator(owners, alloci, envi, histi, [], stats)
simi.setup()
envi.visualize(0)
while simi.tick():
    pass

print("done")
