from abc import abstractmethod, ABC


class AgentGenerator(ABC):
	def __init__(self, dim_x, dim_y, dim_z, dim_t):
		self.dim_x = dim_x
		self.dim_y = dim_y
		self.dim_z = dim_z
		self.dim_t = dim_t

	@abstractmethod
	def reset(self):
		pass

	# list of new Agents to be added into the simulation befor time_step
	@abstractmethod
	def update_agents(self, time_step):
		pass