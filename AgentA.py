from typing import List

from Agent import Agent
from coords import Coords


class AgentA(Agent):
	def __init__(self, start: Coords, target: Coords):
		super().__init__(start, target)
		print(f"{str(self.id)}: {str(start)} ----> {str(target)}")

	def __repr__(self):
		return f"{self.id}"

	def value(self, path: List[Coords])->int:
		if path is None:
			return 0
		return len(path)