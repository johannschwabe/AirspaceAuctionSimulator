from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Environment.Environment import Environment


class Owner(ABC):
    label = "Abstract Owners"
    description = "An Abstract Owners: Override this class variable"
    min_locations: int
    max_locations: int
    meta: []
    allocation_type: str

    def __init__(self, owner_id: str, name: str, color: str):
        self.id: str = owner_id
        self.name: str = name
        self.color: str = color
        self.agents: List["Agent"] = []
        self.total_achieved_welfare: float = 0.
        self.total_optimal_welfare: float = 0.
        self.total_costs: float = 0.
        self._agent_id: int = 0

    def get_agent_id(self):
        agent_id = self._agent_id
        self._agent_id += 1
        return f"{self.id}-{agent_id}"

    @abstractmethod
    def generate_agents(self, t: int, environment: "Environment") -> List["Agent"]:
        pass
