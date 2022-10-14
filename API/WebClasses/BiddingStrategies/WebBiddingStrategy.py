from abc import ABC, abstractmethod
from typing import Dict, List, TYPE_CHECKING, Type

from Simulator import BiddingStrategy

if TYPE_CHECKING:
    from Simulator import ValueFunction


class WebBiddingStrategy(BiddingStrategy, ABC):
    label = "Abstract Bidding Strategy"
    description = "An Bidding Strategy: Override this class variable"
    min_locations: int
    max_locations: int
    allocation_type: str

    @staticmethod
    @abstractmethod
    def compatible_value_functions() -> List[Type["ValueFunction"]]:
        pass

    @staticmethod
    @abstractmethod
    def meta() -> List[Dict]:
        pass
