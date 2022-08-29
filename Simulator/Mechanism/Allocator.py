from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Type

from Simulator.BidTracker.BidTracker import BidTracker

if TYPE_CHECKING:
    from Simulator.Agents.Agent import Agent
    from Simulator.Allocations.Allocation import Allocation
    from Simulator.Environment.Environment import Environment
    from Simulator.Bids.BiddingStrategy import BiddingStrategy


class Allocator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_bid_tracker(self) -> BidTracker | None:
        pass

    @abstractmethod
    def allocate(self,
                 agents: List["Agent"],
                 env: "Environment",
                 tick: int) -> List["Allocation"]:
        pass

    @staticmethod
    @abstractmethod
    def compatible_bidding_strategies() -> List[Type["BiddingStrategy"]]:
        pass

    @staticmethod
    @abstractmethod
    def compatible_payment_functions():
        pass
