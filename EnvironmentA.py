from Agent import Agent
from Environment import Environment


class EnvironmentA(Environment):

    def __init__(self):
        super().__init__()

    def reset(self):
        self.agents = []

    def add_agent(self, agent: Agent, time_step):
        self.agents.append(agent)
        agent.start.t = time_step
        loci = self.get_field(agent.start,
                              creating=True)
        loci.reserved_for = agent

    def move(self):
        pass
