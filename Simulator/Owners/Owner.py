from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Dict, Any

from ..Location.GridLocation import GridLocation

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Environment.Environment import Environment
    from ..Bids.BiddingStrategy import BiddingStrategy
    from ..ValueFunction.ValueFunction import ValueFunction


class Owner(ABC):
    label = "Abstract Owners"
    description = "An Abstract Owners: Override this class variable"
    min_locations: int
    max_locations: int
    config: []
    allocation_type: str

    def __init__(self, owner_id: str,
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction",
                 name: str,
                 color: str,
                 meta: Dict[str, Any],
                 stops: List["GridLocation"],
                 creation_ticks: List[int]):
        self.id: str = owner_id
        self.name: str = name
        self.color: str = color
        self.agents: List["Agent"] = []
        self.total_achieved_welfare: float = 0.
        self.total_optimal_welfare: float = 0.
        self.total_costs: float = 0.
        self._agent_id: int = 0
        self.bidding_strategy = bidding_strategy
        self.value_function = value_function
        self.config = meta
        self.stops = stops
        self.creation_ticks = creation_ticks

    def get_agent_id(self):
        agent_id = self._agent_id
        self._agent_id += 1
        return f"{self.id}-{agent_id}"

    @abstractmethod
    def generate_agents(self, t: int, environment: "Environment") -> List["Agent"]:
        pass
