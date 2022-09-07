from abc import abstractmethod, ABC
from typing import TYPE_CHECKING, List, Type

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Bids.Bid import Bid
    from ..ValueFunction.ValueFunction import ValueFunction
    from ..Environment.Environment import Environment


class BiddingStrategy(ABC):
    label = "Abstract Bidding Strategy"
    description = "An Bidding Strategy: Override this class variable"
    min_locations: int
    max_locations: int
    allocation_type: str

    @staticmethod
    @abstractmethod
    def meta():
        pass

    @abstractmethod
    def generate_bid(self, agent: "Agent", environment: "Environment", time_step: int) -> "Bid":
        pass

    @staticmethod
    @abstractmethod
    def compatible_value_functions() -> List[Type["ValueFunction"]]:
        pass
