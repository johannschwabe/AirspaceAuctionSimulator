from Simulator import ABABid
from PriorityBid import PriorityBid


class PriorityABABid(ABABid, PriorityBid):
    def __init__(self, battery, a, b, priority, flying):
        super(ABABid).__init__(battery, a, b)
        super(PriorityBid).__init__(priority)
        self.flying = flying
