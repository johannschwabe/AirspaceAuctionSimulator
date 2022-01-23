from abc import ABC, abstractmethod
from Agent import Agent


class Environment(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def reset(self):
		pass

	@abstractmethod
	def add_agent(self, agent: Agent):
		pass