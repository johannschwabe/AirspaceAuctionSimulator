from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Bids.Bid import Bid
    from ..Environment.Environment import Environment


class BiddingStrategy(ABC):
    @abstractmethod
    def generate_bid(self, agent: "Agent", environment: "Environment", time_step: int) -> "Bid":
        pass
