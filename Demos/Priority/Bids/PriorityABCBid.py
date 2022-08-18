from AAS import ABCBid
from PriorityBid import PriorityBid


class PriorityABCBid(ABCBid, PriorityBid):
    def __init__(self, battery, locations, stays, priority, flying):
        super(ABCBid).__init__(battery, locations, stays)
        super(PriorityBid).__init__(priority)
        self.flying = flying
