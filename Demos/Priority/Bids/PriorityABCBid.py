from Simulator import ABCBid


class PriorityABCBid(ABCBid):
    def __init__(self, battery, locations, stays, priority, flying):
        super().__init__(battery, locations, stays)
        self.priority = priority
        self.flying = flying
