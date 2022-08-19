from typing import List, TYPE_CHECKING

from .Bid import Bid

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D


class ABCBid(Bid):
    def __init__(self, battery: int, locations: List["Coordinate4D"], stays: List[int]):
        super().__init__(battery)

        self.battery: int = battery
        self.locations: List["Coordinate4D"] = locations
        self.stays: List[int] = stays
