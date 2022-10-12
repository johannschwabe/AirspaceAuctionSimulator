from abc import abstractmethod, ABC
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from ..Allocations.Allocation import Allocation
    from ..BidTracker.BidTracker import BidTracker
    from ..Agents.Agent import Agent
    from ..Environment.Environment import Environment


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
        pass
