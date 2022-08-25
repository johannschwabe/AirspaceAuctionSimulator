from abc import abstractmethod, ABC
from typing import List

from Simulator.Allocations.Allocation import Allocation


class PaymentRule(ABC):
    @abstractmethod
    def calculate_payments(self, allocations: List[Allocation]):
        pass
