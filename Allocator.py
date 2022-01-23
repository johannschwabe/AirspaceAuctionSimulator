from abc import ABC, abstractmethod

from Environment import Environment


class Allocator(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def reset(self):
		pass

	@abstractmethod
	def allocate(self, env: Environment):
		pass