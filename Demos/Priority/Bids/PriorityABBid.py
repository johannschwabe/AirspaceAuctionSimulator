from Simulator import ABBid, Coordinate4D
from PriorityBid import PriorityBid


class PriorityABBid(ABBid, PriorityBid):
    def __init__(self, battery: int, a: Coordinate4D, b: Coordinate4D, priority: float, flying: bool):
        super(ABBid).__init__(battery, a, b)
        super(PriorityBid).__init__(priority)
        self.flying = flying
