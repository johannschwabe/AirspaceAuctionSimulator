from typing import List

from Simulator import Agent, Environment, Owner
from agents.AgentB import AgentB


class OwnerB(Owner):
    def __init__(self, creation_ticks: List[int]):
        super().__init__()
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: Environment) -> List[Agent]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            res.append(AgentB(env.dimension, t))

        self.agents += res
        return res
