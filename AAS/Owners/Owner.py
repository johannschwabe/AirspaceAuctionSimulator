from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Simulator import Simulator


class Owner(ABC):
    label = "Abstract Owners"
    description = "An Abstract Owners: Override this class variable"
    min_locations: int
    max_locations: int
    meta: []
    allocation_type: str

    def __init__(self, name: str, color: str):
        self.name: str = name
        self.color: str = color
        self.agents: List["Agent"] = []
        self.total_achieved_welfare: float = 0.
        self.total_optimal_welfare: float = 0.
        self.total_costs: float = 0.

    @abstractmethod
    def generate_agents(self, t: int, simulator: "Simulator") -> List["Agent"]:
        pass
