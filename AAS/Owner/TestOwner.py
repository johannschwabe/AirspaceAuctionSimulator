from typing import List, TYPE_CHECKING

from . import Owner
from ..Agent import ABCAgent

if TYPE_CHECKING:
    from AAS import Environment
    from AAS.Agent import Agent


class TestOwner(Owner):
    def __init__(self, name: str, color: str, locations):
        super().__init__(name, color)
        self.locations = locations

    def generate_agents(self, t: int, env: "Environment") -> List["Agents"]:
        if t == 0:
            self.agents = [ABCAgent(self.locations, len(self.locations) * [0])]
            return self.agents
        return []
