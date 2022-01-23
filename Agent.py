from abc import ABC


class Agent(ABC):
	id = 0
	def __init__(self, x, y, z, t):
		self.x = x
		self.y = y
		self.z = z
		self.t = t
		self.id = Agent.id
		Agent.id += 1

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_z(self):
		return self.z

	def get_t(self):
		return self.t