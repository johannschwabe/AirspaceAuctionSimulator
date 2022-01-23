from AgentGeneratorA import AgentGeneratorA
from AgentGeneratorB import AgentGeneratorB
from AllocatorA import AllocatorA
from EnvironmentA import EnvironmentA
from History import History
from Simulator import Simulator
from coords import Coords

Coords.dim_x = 10
Coords.dim_y = 10
Coords.dim_z = 1
Coords.dim_t = 100
alloci = AllocatorA()
envi = EnvironmentA()
agentGeni = AgentGeneratorB(envi)
histi = History()
simi = Simulator(agentGeni, alloci, envi, histi)


envi.block(Coords(0,4,0,0))
envi.block(Coords(1,4,0,0))
envi.block(Coords(3,4,0,0))

envi.block(Coords(0,6,0,0))
envi.block(Coords(1,6,0,0))
envi.block(Coords(2,6,0,0))
envi.block(Coords(3,6,0,0))

envi.block(Coords(3,1,0,0))
envi.block(Coords(3,2,0,0))
envi.block(Coords(3,7,0,0))
envi.block(Coords(3,9,0,0))

envi.block(Coords(5,1,0,0))
envi.block(Coords(5,2,0,0))
envi.block(Coords(5,3,0,0))
envi.block(Coords(5,5,0,0))
envi.block(Coords(5,6,0,0))

envi.block(Coords(5,8,0,0))
envi.block(Coords(5,9,0,0))

envi.visualize(0)
for _ in range(50):
	simi.tick()

print("done")