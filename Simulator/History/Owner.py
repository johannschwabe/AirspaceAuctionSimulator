import random

from typing import List
from .Agent import Agent

r = lambda: random.randint(0, 255)


class Owner:

    def __init__(self):
        self.agents: List[Agent] = []
        self.total_welfare: float = 0.0
        self.total_costs: float = 0.
        self.color: str = '#%02X%02X%02X' % (r(), r(), r())

    def add_agent(self, agent: Agent):
        self.agents.append(agent)
        self.total_welfare += agent.welfare
        self.total_costs += agent.costs
