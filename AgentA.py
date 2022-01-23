from Agent import Agent
from coords import Coords


class AgentA(Agent):
	def __init__(self, start: Coords, target: Coords):
		super().__init__(start, target)

