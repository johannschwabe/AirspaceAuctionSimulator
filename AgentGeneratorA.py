from AgentGenerator import AgentGenerator
from AgentA import AgentA

class AgentGeneratorA(AgentGenerator):

	def __init__(self, dim_x, dim_y, dim_z, dim_t):
		super().__init__(dim_x, dim_y, dim_z, dim_t)

		self.agents = [
			[AgentA(1,1,0,0)],
			[],
			[],
			[],
			[AgentA(5, 5, 0, 4)],
		]

	def reset(self):
		pass

	def update_agents(self, time_step):
		if time_step < len(self.agents):
			return self.agents[time_step]
		return []
