from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from ..Agents.AgentType import AgentType
from ..Owners.Owner import Owner

if TYPE_CHECKING:
    from ..Agents.PathAgent import PathAgent
    from ..Environment.Environment import Environment
    from ..Bids.BiddingStrategy import BiddingStrategy
    from ..ValueFunction.ValueFunction import ValueFunction


class PathOwner(Owner, ABC):
    allocation_type: str = AgentType.PATH.value

    def __init__(self,
                 owner_id: str,
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction",
                 config: Optional[Dict[str, Any]] = None):
        super().__init__(owner_id, bidding_strategy, value_function, config)

    @abstractmethod
    def generate_agents(self, t: int, environment: "Environment") -> List["PathAgent"]:
        pass
