import random
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

from ..Agent import Agent
from ..Coordinate import Coordinate4D
from ..Environment import Environment


class Owner(ABC):
    _id: int = 10000

    def __init__(self, name: str, color: str):
        self.name: str = name
        self.color: str = color
        self.agents: List[Agent] = []
        self.total_achieved_welfare: float = 0.
        self.total_optimal_welfare: float = 0.
        self.total_costs: float = 0.
        self.id: int = Owner._id
        Owner._id += 1

    @abstractmethod
    def generate_agents(self, t: int, env: Environment) -> List[Agent]:
        pass
