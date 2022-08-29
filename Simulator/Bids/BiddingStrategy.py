from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Bids.Bid import Bid
    from ..Environment.Environment import Environment


class BiddingStrategy(ABC):
    label = "Abstract Bidding Strategy"
    description = "An Bidding Strategy: Override this class variable"
    min_locations: int
    max_locations: int
    meta: []
    allocation_type: str

    @abstractmethod
    def generate_bid(self, agent: "Agent", environment: "Environment", time_step: int) -> "Bid":
        pass
