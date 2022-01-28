from AgentGeneratorA import AgentGeneratorA
from AgentGeneratorB import AgentGeneratorB
from AllocatorA import AllocatorA
from EnvironmentA import EnvironmentA
from History import History
from Simulator import Simulator
from Statistics import Statistics
from coords import Coords

Coords.dim_x = 10
Coords.dim_y = 10
Coords.dim_z = 1
Coords.dim_t = 100
envi = EnvironmentA()
stati = Statistics()
alloci = AllocatorA(envi, stati)
agentGeni = AgentGeneratorA(envi)
histi = History()
simi = Simulator(agentGeni, alloci, envi, histi)



envi.block(Coords(3,6,0,0))

envi.block(Coords(3,1,0,0))
envi.block(Coords(3,2,0,0))
envi.block(Coords(3,3,0,0))
envi.block(Coords(3,4,0,0))
envi.block(Coords(3,5,0,0))
envi.block(Coords(3,6,0,0))
envi.block(Coords(3,7,0,0))
envi.block(Coords(3,8,0,0))
envi.block(Coords(3,9,0,0))

envi.block(Coords(5,1,0,0))
envi.block(Coords(5,2,0,0))
envi.block(Coords(5,3,0,0))
envi.block(Coords(5,4,0,0))
envi.block(Coords(5,5,0,0))
envi.block(Coords(5,6,0,0))
envi.block(Coords(5,7,0,0))
envi.block(Coords(5,8,0,0))
envi.block(Coords(5,9,0,0))

envi.visualize(0)
for _ in range(50):
	simi.tick()

print(stati)
print("done")