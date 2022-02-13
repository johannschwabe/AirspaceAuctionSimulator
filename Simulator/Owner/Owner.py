from abc import ABC, abstractmethod
from typing import List

from ..Agent import Agent
from ..Environment import Environment


class Owner(ABC):
    def __init__(self):
        self.agents: List[Agent] = []

    @abstractmethod
    def generate_agents(self, t: int, env: Environment) -> List[Agent]:
        pass
