from Simulator.Bids.ABBid import ABBid


class PriorityABBid(ABBid):
    def __init__(self, battery, a, b, priority, flying):
        super().__init__(battery, a, b)
        self.priority = priority
        self.flying = flying
