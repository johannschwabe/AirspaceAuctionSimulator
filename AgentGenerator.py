from abc import abstractmethod, ABC


class AgentGenerator(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def reset(self):
		pass

	# list of new Agents to be added into the simulation befor time_step
	@abstractmethod
	def update_agents(self, time_step):
		pass