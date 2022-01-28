from abc import ABC, abstractmethod
from typing import List

from Agent import Agent
from Environment import Environment
from Statistics import Statistics


class Allocator(ABC):
	def __init__(self, env: Environment, stats: Statistics):
		self.env = env
		self.stats = stats

	@abstractmethod
	def reset(self):
		pass

	def get_env(self):
		return self.env


	def allocate(self, new_agents: List[Agent]):
		pass