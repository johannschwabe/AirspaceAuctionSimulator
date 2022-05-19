from Simulator.Bid import ABBid
from Simulator.Coordinate import TimeCoordinate


class BiddingABBid(ABBid):
    def __init__(self, battery: int, a: TimeCoordinate, b: TimeCoordinate, priority: float):
        super().__init__(battery, a, b)
        self.priority = priority
