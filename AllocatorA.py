from Allocator import Allocator
from Environment import Environment


class AllocatorA(Allocator):
	def __init__(self):
		super().__init__()

	def allocate(self, env: Environment, new_agents):
		for agent in new_agents:
			path = env.astar(agent.start, agent.target, agent)
			if not path:
				return
			for coord in path:
				field = env.get_field(coord, True)
				field.reserved_for = agent

	def reset(self):
		pass
