import random
from typing import List

from Simulator import Agent, Environment, Owner
from agents.JohannAgent import JohannAgent


class JohannOwner(Owner):
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
                agent = JohannAgent(env.dimension, t)
                res.append(agent)
                print(f"Johann created {agent}")

            self.agents += res
        return res
