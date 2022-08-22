from Simulator import ABABid


class PriorityABABid(ABABid):
    def __init__(self, battery, a, b, priority, flying, stay):
        super().__init__(battery, a, b, stay)
        self.priority = priority
        self.flying = flying
