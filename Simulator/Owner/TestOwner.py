import random
from typing import List, TYPE_CHECKING

from ..Coordinate import TimeCoordinate
from .Owner import Owner
from ..Agent import ABAgent, ABCAgent

if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Agent import Agent


class TestOwner(Owner):
    def __init__(self, name: str, color: str, locations):
        super().__init__(name, color)
        self.locations = locations

    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        if t == 0:
            return [ABCAgent(self.locations, len(self.locations)*[0])]
        return []
