from Simulator import Bid


class PrioritySpaceBid(Bid):
    def __init__(self, agent, priority):
        super().__init__(agent)
        self.priority = priority
