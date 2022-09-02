from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Allocations.Allocation import Allocation
    from ..Environment.Environment import Environment
    from ..BidTracker.BidTracker import BidTracker


class Allocator(ABC):
    """
    Provides the allocate function that generates new allocations for agents.
    """

    @abstractmethod
    def get_bid_tracker(self) -> "BidTracker":
        """
        Returns the active bid-tracker
        :return:
        """
        pass

    @abstractmethod
    def allocate(self, agents: List["Agent"], env: "Environment", tick: int) -> Dict["Agent", "Allocation"]:
        """
        Generate new allocations for agents.
        Can generate new allocations for all agents in the environment not just the provided new agents.
        :param agents:
        :param env:
        :param tick:
        :return:
        """
        pass

    @staticmethod
    @abstractmethod
    def compatible_owner():
        """
        Returns all Owners that are compatible with this allocator.
        :return:
        """
        pass

    @staticmethod
    def wants_to_reallocate(_environment: "Environment", _tick: int):
        """
        Returns `True` if the allocator wants to reallocate despite no new agents arrived.
        :return:
        """
        return False
