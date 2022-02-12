from typing import List

from ..Agent import Agent
from ..Environment import Environment


class Owner:
    def __init__(self):
        self.agents: List[Agent] = []

    def generate_agents(self, t: int, env: Environment) -> List[Agent]:
        pass

    def get_welfare(self, t1: int, t2: int) -> float:
        pass
