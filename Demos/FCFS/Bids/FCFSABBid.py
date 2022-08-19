from Simulator import ABBid, Coordinate4D


class FCFSABBid(ABBid):
    def __init__(self, battery: int, a: Coordinate4D, b: Coordinate4D):
        super().__init__(battery, a, b)
