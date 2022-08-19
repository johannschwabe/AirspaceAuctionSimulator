from Demos.Priority.Bids.PriorityBid import PriorityBid
from Simulator.Bids.ABBid import ABBid


class PriorityABBid(ABBid, PriorityBid):
    def __init__(self, battery, a, b, priority, flying):
        super(ABBid).__init__(battery, a, b)
        super(PriorityBid).__init__(priority)
        self.flying = flying
