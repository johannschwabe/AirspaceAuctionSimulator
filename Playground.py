from AgentGeneratorA import AgentGeneratorA
from AllocatorA import AllocatorA
from EnvironmentA import EnvironmentA
from Simulator import Simulator

agentGeni = AgentGeneratorA(10,10,0,100)
alloci = AllocatorA()
envi = EnvironmentA(10,10,0,100)
simi = Simulator(agentGeni, alloci, envi)

