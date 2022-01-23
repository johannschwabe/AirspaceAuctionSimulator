from abc import ABC, abstractmethod
from Agent import Agent


class Environment(ABC):
	def __init__(self, dim_x, dim_y, dim_z, dim_t):
		self.dim_x = dim_x
		self.dim_y = dim_y
		self.dim_z = dim_z
		self.dim_t = dim_t
		self.agents = []

	@abstractmethod
	def reset(self):
		pass

	@abstractmethod
	def add_agent(self, agent: Agent, time_step):
		pass

	@abstractmethod
	def move(self):
		pass