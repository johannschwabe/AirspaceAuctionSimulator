from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Environment.Environment import Environment
    from ..Bids.BiddingStrategy import BiddingStrategy
    from ..ValueFunction.ValueFunction import ValueFunction


class Owner(ABC):
    allocation_type: str

    def __init__(self,
                 owner_id: str,
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction",
                 config: Optional[Dict[str, Any]]):
        self.id: str = owner_id
        self.agents: List["Agent"] = []
        self.total_achieved_welfare: float = 0.
        self.total_optimal_welfare: float = 0.
        self.total_costs: float = 0.
        self._agent_id: int = 0
        self.bidding_strategy = bidding_strategy
        self.value_function = value_function
        self.config: Dict[str, Any] = config if config is not None else {}

    def get_agent_id(self):
        agent_id = self._agent_id
        self._agent_id += 1
        return f"{self.id}-{agent_id}"

    @abstractmethod
    def generate_agents(self, t: int, environment: "Environment") -> List["Agent"]:
        pass
