from typing import List, TYPE_CHECKING

from Simulator.Bid import StationaryBid
if TYPE_CHECKING:
    from Simulator.Coordinate import TimeCoordinate


class BiddingStationaryBid(StationaryBid):
    def __init__(self, blocks: List[List["TimeCoordinate"]], priority: float):
        super().__init__(blocks)
        self.priority = priority
