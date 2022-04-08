import random
from abc import ABC, abstractmethod
from typing import List

from ..Agent import Agent
from ..Environment import Environment


def r(): return random.randint(0, 255)


class Owner(ABC):
    id: int = 0

    def __init__(self, name: str):
        self.name: str = name
        self.agents: List[Agent] = []
        self.total_achieved_welfare: float = 0.
        self.total_optimal_welfare: float = 0.
        self.total_costs: float = 0.
        self.color: str = '#%02X%02X%02X' % (r(), r(), r())
        self.id: int = Owner.id
        Owner.id += 1

    @abstractmethod
    def generate_agents(self, t: int, env: Environment) -> List[Agent]:
        pass
