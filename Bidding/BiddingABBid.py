from Simulator.Bid import ABBid
from Simulator.Coordinate import Coordinate4D


class BiddingABBid(ABBid):
    def __init__(self, battery: int, a: Coordinate4D, b: Coordinate4D, priority: float, flying: bool):
        super().__init__(battery, a, b)
        self.priority = priority
        self.flying = flying
