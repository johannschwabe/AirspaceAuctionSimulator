from abc import ABC, abstractmethod
from typing import List, Type

from Simulator import Allocator, PaymentRule
from ..BiddingStrategies.WebBiddingStrategy import WebBiddingStrategy


class WebAllocator(ABC, Allocator):
    @staticmethod
    @abstractmethod
    def compatible_bidding_strategies() -> List[Type["WebBiddingStrategy"]]:
        pass

    @staticmethod
    @abstractmethod
    def compatible_payment_functions() -> List[Type["PaymentRule"]]:
        pass
