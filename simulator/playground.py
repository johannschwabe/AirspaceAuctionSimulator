from simulator.owners.OwnerB import OwnerB
from simulator.allocators.AllocatorA import AllocatorA
from simulator.environments.EnvironmentA import EnvironmentA
from simulator.helpers.History import History
from Simulator import Simulator
from simulator.coordinates.Coordinates import Coordinates

Coordinates.dim_x = 10
Coordinates.dim_y = 10
Coordinates.dim_z = 1
Coordinates.dim_t = 100
alloci = AllocatorA()
envi = EnvironmentA()
agentGeni = OwnerB(envi)
histi = History()
simi = Simulator(agentGeni, alloci, envi, histi)

envi.block(Coordinates(0, 4, 0, 0))
envi.block(Coordinates(1, 4, 0, 0))
envi.block(Coordinates(3, 4, 0, 0))

envi.block(Coordinates(0, 6, 0, 0))
envi.block(Coordinates(1, 6, 0, 0))
envi.block(Coordinates(2, 6, 0, 0))
envi.block(Coordinates(3, 6, 0, 0))

envi.block(Coordinates(3, 1, 0, 0))
envi.block(Coordinates(3, 2, 0, 0))
envi.block(Coordinates(3, 7, 0, 0))
envi.block(Coordinates(3, 9, 0, 0))

envi.block(Coordinates(5, 1, 0, 0))
envi.block(Coordinates(5, 2, 0, 0))
envi.block(Coordinates(5, 3, 0, 0))
envi.block(Coordinates(5, 5, 0, 0))
envi.block(Coordinates(5, 6, 0, 0))

envi.block(Coordinates(5, 8, 0, 0))
envi.block(Coordinates(5, 9, 0, 0))

envi.visualize(0)
for _ in range(50):
    simi.tick()

print("done")
