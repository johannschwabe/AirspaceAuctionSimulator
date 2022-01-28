from abc import ABC, abstractmethod
from typing import List
from coords import Coords


class Agent(ABC):
	id = 0
	def __init__(self, start: Coords, target: Coords):
		self.start = start
		self.target = target
		self.id = Agent.id
		Agent.id += 1

	@abstractmethod
	def value(self, path:List[Coords]):
		pass