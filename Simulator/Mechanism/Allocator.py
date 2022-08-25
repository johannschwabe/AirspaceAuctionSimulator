from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from Simulator.Bids.Bid import Bid

if TYPE_CHECKING:
    from Simulator.Allocations.Allocation import Allocation
    from Simulator.Environment.Environment import Environment


class Allocator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def allocate(self,
                 bids: List["Bid"],
                 env: "Environment",
                 tick: int) -> List["Allocation"]:
        pass

    @staticmethod
    def compatible_owner():
        pass
