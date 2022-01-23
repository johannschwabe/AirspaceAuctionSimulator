from AgentGenerator import AgentGenerator
from AgentA import AgentA
from coords import Coords


class AgentGeneratorA(AgentGenerator):

	def __init__(self):
		super().__init__()

		self.agents = [
			[AgentA(Coords(1,1,0,0),Coords(8,6,0,0))],
			[],
			[],
			[],
			[AgentA(Coords(5, 5, 0, 4),Coords(8,7,0,0))],
		]

	def reset(self):
		pass

	def update_agents(self, time_step):
		if time_step < len(self.agents):
			return self.agents[time_step]
		return []

