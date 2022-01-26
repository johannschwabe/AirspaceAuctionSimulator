from Agent import Agent
from Coords import Coords


class AgentA(Agent):
	def __init__(self, start: Coords, target: Coords):
		super().__init__(start, target)
		print(f"{str(self.id)}: {str(start)} ----> {str(target)}")
