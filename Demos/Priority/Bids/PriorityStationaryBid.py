from Demos.Priority.Bids.PriorityBid import PriorityBid
from Simulator.Bids.StationaryBid import StationaryBid


class PriorityStationaryBid(StationaryBid, PriorityBid):
    def __init__(self, blocks, priority):
        super(StationaryBid).__init__(blocks)
        super(PriorityBid).__init__(priority)
