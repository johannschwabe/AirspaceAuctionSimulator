from abc import abstractmethod, ABC
from typing import List

from Simulator.Allocations.Allocation import Allocation
from Simulator.BidTracker.BidTracker import BidTracker


class PaymentRule(ABC):
    @abstractmethod
    def calculate_payments(self, allocations: List[Allocation], bid_tracker: BidTracker):
        pass
