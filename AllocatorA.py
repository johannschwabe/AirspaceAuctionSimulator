from Allocator import Allocator
from Environment import Environment
from Helpers import astar
from Statistics import Statistics
from coords import Coords


class AllocatorA(Allocator):
	def __init__(self, env: Environment, stats: Statistics):
		super().__init__(env, stats)

	def allocate(self, new_agents):
		env = self.get_env()
		for agent in new_agents:
			path = astar(env, agent.start, agent.target, agent)
			best_path = astar(env, agent.start, agent.target, agent, ignore_reservations=True)
			achieved_value = agent.value(path)
			max_value = agent.value(best_path)
			self.stats.add_value(agent, achieved_value, max_value)
			if not path:
				return
			for coord in path:
				field = env.get_field(coord, True)
				field_later = env.get_field(Coords(coord.x, coord.y, coord.z, coord.t-1), True)
				field_later.reserved_for = agent
				field.reserved_for = agent

	def reset(self):
		pass
