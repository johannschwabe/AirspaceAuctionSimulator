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


# envi.get_field(Coords(1,2,0,0),True).reserved_for = envi.agents[0]
envi.block(Coords(0,2,0,0))
envi.block(Coords(1,2,0,0))
envi.block(Coords(2,2,0,0))
envi.block(Coords(3,2,0,0))

for _ in range(10):
	simi.tick()
