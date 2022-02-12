import random
from typing import List

from Simulator import Agent, Environment, Owner
from agents.AgentA import AgentA


class OwnerA(Owner):
    def __init__(self):
        super().__init__()
        self.nr_agents = random.randint(5, 10)

    def generate_agents(self, t: int, env: Environment) -> List[Agent]:
        res = []
        if len(self.agents) < self.nr_agents:
            options = [0, 0, 0, 1, 1, 1, 2, 2, 3]
            random.shuffle(options)
            nr_new_agents = max(min(options[0], self.nr_agents - len(self.agents)), 0)
            for _ in range(nr_new_agents):
                res.append(AgentA(env.dimension, t))
            self.agents += res
        return res
