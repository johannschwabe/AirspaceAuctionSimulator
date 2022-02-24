from typing import List
from .Agent import Agent


class Owner:

    def __init__(self):
        self.agents: List[Agent] = []
        self.total_welfare: float = 0.0
        self.total_costs: float = 0.0

    def add_agent(self, agent: Agent):
        self.agents.append(agent)
        self.total_welfare += agent.welfare
        self.total_costs += agent.costs

