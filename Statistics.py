from Agent import Agent


class Statistics:
	def __init__(self):
		self.valuations = {}

	def add_value(self, agent: Agent, achieved_value, max_value):
		self.valuations[agent] = {"achieved_value": achieved_value, "max_value": max_value}

	def __str__(self):
		res = f"agent:\tachieved\tmax\n"
		for key, value in self.valuations.items():
			res += f"{key}:\t{value['achieved_value']}\t{value['max_value']}\n"
		return res