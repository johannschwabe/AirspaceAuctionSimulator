from Simulator import ABCBid


class FCFSABCBid(ABCBid):
    def __init__(self, battery, locations, stays):
        super().__init__(battery, locations, stays)
