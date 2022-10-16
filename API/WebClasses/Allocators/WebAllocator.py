from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING, Type

from Simulator import Allocator

if TYPE_CHECKING:
    from Simulator import PaymentRule
    from API.WebClasses.BiddingStrategies.WebBiddingStrategy import WebBiddingStrategy


class WebAllocator(Allocator, ABC):
    @staticmethod
    @abstractmethod
    def compatible_bidding_strategies() -> List[Type["WebBiddingStrategy"]]:
        pass

    @staticmethod
    @abstractmethod
    def compatible_payment_functions() -> List[Type["PaymentRule"]]:
        pass
