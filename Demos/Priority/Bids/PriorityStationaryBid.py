from Simulator.Bids.StationaryBid import StationaryBid


class PriorityStationaryBid(StationaryBid):
    def __init__(self, blocks, priority):
        super().__init__(blocks)
        self.priority = priority
