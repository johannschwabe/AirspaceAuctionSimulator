from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .Owner import Owner
from ..Agents.AgentType import AgentType

if TYPE_CHECKING:
    from ..Agents.SpaceAgent import SpaceAgent
    from ..Environment.Environment import Environment
    from ..Bids.BiddingStrategy import BiddingStrategy
    from ..ValueFunction.ValueFunction import ValueFunction


class SpaceOwner(Owner, ABC):
    allocation_type: str = AgentType.SPACE.value

    def __init__(self,
                 owner_id: str,
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction",
                 config: Optional[Dict[str, Any]] = None):
        super().__init__(owner_id, bidding_strategy, value_function, config)

    @abstractmethod
    def generate_agents(self, t: int, environment: "Environment") -> List["SpaceAgent"]:
        pass
