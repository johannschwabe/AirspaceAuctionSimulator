import random

from AgentGenerator import AgentGenerator
from AgentA import AgentA
from Environment import Environment
from coords import Coords


class AgentGeneratorB(AgentGenerator):

	def __init__(self, env: Environment):
		super().__init__(env)
		self.probs = [0,0,1,0,2]

	def reset(self):
		pass

	def update_agents(self, time_step):
		if time_step > 30:
			return []
		nr = random.choice(self.probs)
		res = []
		for _ in range(nr):
			coordis = []
			while len(coordis) < 2:
				x = random.randint(0,Coords.dim_x - 1)
				y = random.randint(0,Coords.dim_y - 1)
				z = random.randint(0,Coords.dim_z - 1)
				coordi = Coords(x,y,z,time_step)
				field = self.env.get_field(coordi, False)
				if field is None or (not field.blocked and field.reserved_for is None):
					coordis.append(coordi)

			res.append(AgentA(coordis[0], coordis[1]))
		return res
