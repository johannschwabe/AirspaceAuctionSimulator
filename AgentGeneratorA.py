from AgentGenerator import AgentGenerator
from AgentA import AgentA
from Coords import Coords


class AgentGeneratorA(AgentGenerator):

    def __init__(self, env):
        super().__init__(env)

        self.agents = [
            [AgentA(Coords(0, 5, 0, 0), Coords(4, 1, 0, 0)), AgentA(Coords(4, 9, 0, 0), Coords(4, 1, 0, 0))],

        ]

    def reset(self):
        pass

    def update_agents(self, time_step):
        if time_step < len(self.agents):
            return self.agents[time_step]
        return []
