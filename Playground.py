from AgentGeneratorA import AgentGeneratorA
from AllocatorA import AllocatorA
from EnvironmentA import EnvironmentA
from Simulator import Simulator
from coords import Coords

Coords.dim_x = 10
Coords.dim_y = 10
Coords.dim_z = 1
Coords.dim_t = 100
agentGeni = AgentGeneratorA()
alloci = AllocatorA()
envi = EnvironmentA()
simi = Simulator(agentGeni, alloci, envi)


envi.block(Coords(0,4,0,0))
envi.block(Coords(1,4,0,0))
envi.block(Coords(2,4,0,0))
envi.block(Coords(3,4,0,0))

envi.block(Coords(0,6,0,0))
envi.block(Coords(1,6,0,0))
envi.block(Coords(2,6,0,0))
envi.block(Coords(3,6,0,0))

envi.block(Coords(3,1,0,0))
envi.block(Coords(3,2,0,0))
envi.block(Coords(3,3,0,0))
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
for _ in range(10):
	simi.tick()
