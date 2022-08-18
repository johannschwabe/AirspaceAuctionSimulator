from AAS import StationaryBid, Coordinate4D
from PriorityBid import PriorityBid


class PriorityStationaryBid(StationaryBid, PriorityBid):
    def __init__(self, blocks: List[List[Coordinate4D]], priority: float):
        super(StationaryBid).__init__(blocks)
        super(PriorityBid).__init__(priority)
