from typing import List
from simulator.agents.Agent import Agent


class Owner:
    def __init__(self):
        self.agents: List[Agent] = []

    def generate_agents(self, t: int) -> List[Agent]:
        pass

    def get_welfare(self, t1: int, t2: int) -> float:
        pass
