from Simulator import SpaceBid


class PrioritySpaceBid(SpaceBid):
    def __init__(self, blocks, priority):
        super().__init__(blocks)
        self.priority = priority
