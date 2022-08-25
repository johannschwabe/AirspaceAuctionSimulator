from Simulator import Bid


class PriorityPathBid(Bid):
    def __init__(self, agent, priority, flying):
        super().__init__(agent)
        self.priority = priority
        self.flying = flying
