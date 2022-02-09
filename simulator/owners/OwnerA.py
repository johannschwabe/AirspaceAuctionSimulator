import random
from typing import List

from simulator.agents.Agent import Agent
from simulator.agents.AgentA import AgentA
from simulator.environments.Environment import Environment
from simulator.owners.Owner import Owner


class OwnerA(Owner):
    def __init__(self, env: Environment):
        super().__init__(env)
        self.nr_agents = random.randint(1,7)

    def generate_agents(self, t: int) -> List[Agent]:
        res = []
        if len(self.agents) < self.nr_agents:
            options = [0,0,0,1,1,1,2,2]
            random.shuffle(options)
            nr_new_agents = min(options[0], self.nr_agents - len(self.agents))
            for _ in range(nr_new_agents):
                res.append(AgentA(self.env.dimension, t))
        return res
