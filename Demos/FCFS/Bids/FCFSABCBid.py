from AAS import ABCBid, Coordinate4D


class FCFSABCBid(ABCBid):
    def __init__(self, battery: int, locations: list[Coordinate4D], stays: list[int]):
        super().__init__(battery, locations, stays)
