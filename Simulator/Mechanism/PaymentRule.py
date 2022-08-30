from abc import abstractmethod, ABC
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Allocations.Allocation import Allocation
    from ..BidTracker.BidTracker import BidTracker


class PaymentRule(ABC):
    @abstractmethod
    def calculate_payments(self, allocations: List["Allocation"], bid_tracker: "BidTracker"):
        pass
