from AgentGeneratorA import AgentGeneratorA
from AllocatorA import AllocatorA
from EnvironmentA import EnvironmentA
from Simulator import Simulator

agentGeni = AgentGeneratorA(20,20,1,100)
alloci = AllocatorA()
envi = EnvironmentA(20,20,1,100)
simi = Simulator(agentGeni, alloci, envi)

simi.tick()

envi.get_field(1,2,0,0,True).reserved_for = envi.agents[0]
envi.get_field(2,2,0,0,True).blocked = True

envi.visualize(0)