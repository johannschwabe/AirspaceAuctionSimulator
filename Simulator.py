import Agent as Agent
from AgentGenerator import AgentGenerator
from Allocator import Allocator
from Environment import Environment


class Simulator:
	def __init__(self, agent_generator: AgentGenerator, allocator: Allocator, env: Environment):
		self.agentGenerator = agent_generator
		self.allocator = allocator
		self.env = env
		self.time_step = 0

	def reset(self):
		self.agentGenerator.reset()
		self.allocator.reset()
		self.env.reset()

	def tick(self):
		new_agents = self.agentGenerator.update_agents(self.time_step)
		for agent in new_agents:
			self.env.add_agent(agent, self.time_step)
		self.allocator.allocate(self.env, new_agents)
		self.env.move()
		self.env.visualize(self.time_step)
		self.time_step += 1