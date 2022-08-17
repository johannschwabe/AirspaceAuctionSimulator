from typing import List, TYPE_CHECKING

from AAS.Bid import StationaryBid

if TYPE_CHECKING:
    from AAS.Coordinates import Coordinate4D


class BiddingStationaryBid(StationaryBid):
    def __init__(self, blocks: List[List["Coordinate4D"]], priority: float):
        super().__init__(blocks)
        self.priority = priority
