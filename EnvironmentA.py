from Agent import Agent
from Environment import Environment
from Field import Field


class EnvironmentA(Environment):

	def __init__(self, dim_x, dim_y, dim_z, dim_t):
		super().__init__()
		self.field = {}         # x_y_z_t -> Field

	def reset(self):
		self.agents = []

	def get_field(self, x, y, z, t, creating):
		if not self.field[f"{x}_{y}_{z}_{t}"]:
			if creating:
				new_field = Field()
				self.field[f"{x}_{y}_{z}_{t}"] = new_field
			else:
				return None
		return self.field[f"{x}_{y}_{z}_{t}"]

	def add_agent(self, agent: Agent, time_step):
		self.agents.append(agent)
		loci = self.get_field(agent.get_x(),
		                      agent.get_y(),
		                      agent.get_z(),
		                      time_step,
		                      creating=True)
		loci.occupied_by_agent = agent

	def visualize(self, t):
		for z in range(self.dim_z):
			for x in range(self.dim_x):
				for y in range(self.dim_y):
					field = self.get_field(x,y,z,t, False)
					if field:
						if field.occupied_by_agent:
							print(f"|{field.occupied_by_agent.id}|", end="")
						elif field.reserved_for:
							print(f"{field.reserved_for.id} ", end="")
						elif field.blocked:
							print("_", end="")
					else:
						print(". ", end="")
				print("")
			print("")
		print("")

	def move(self):
		pass

