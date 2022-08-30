from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Allocations.Allocation import Allocation
    from ..Environment.Environment import Environment
    from ..BidTracker.BidTracker import BidTracker


class Allocator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_bid_tracker(self) -> "BidTracker":
        pass

    @abstractmethod
    def allocate(self,
                 agents: List["Agent"],
                 env: "Environment",
                 tick: int) -> List["Allocation"]:
        pass

    @staticmethod
    def compatible_owner():
        pass
