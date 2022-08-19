from Simulator import ABCBid, Coordinate4D


class FCFSABCBid(ABCBid):
    def __init__(self, battery: int, locations: List[Coordinate4D], stays: List[int]):
        super().__init__(battery, locations, stays)
