from abc import ABC, abstractmethod
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from Simulator.Allocations.Allocation import Allocation
    from Simulator.Bids.BidTracker import BidTracker
    from Simulator.Agents.Agent import Agent
    from Simulator.Environment.Environment import Environment


class PaymentRule(ABC):
    """
    Provides function to calculate payments. May be configurable.
    """

    label: str

    @abstractmethod
    def calculate_preliminary_payments(self, allocations: Dict["Agent", "Allocation"], bid_tracker: "BidTracker"):
        """
        Calculate payments for allocations. Directly writes to payment field of the allocation.
        :param allocations:
        :param bid_tracker:
        :return:
        """
        pass

    @abstractmethod
    def calculate_final_payments(self, environment: "Environment", bid_tracker: "BidTracker") -> Dict[int, float]:
        """
        :param environment: the environment with allocated agents
        :param bid_tracker: the bid tracker with all (relevant) past agent bids from the allocator
        :return: A dictionary mapping agent hashes to payments
        """
        pass
