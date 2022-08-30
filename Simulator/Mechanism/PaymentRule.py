from abc import abstractmethod, ABC
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Allocations.Allocation import Allocation
    from ..BidTracker.BidTracker import BidTracker
    from Simulator.Environment.Environment import Environment


class PaymentRule(ABC):
    label: str

    @abstractmethod
    def calculate_preliminary_payments(self, allocations: List["Allocation"], bid_tracker: "BidTracker"):
        pass

    @abstractmethod
    def calculate_final_payments(self, environment: "Environment", bid_tracker: "BidTracker"):
        pass
