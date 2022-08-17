from AAS import ABABid, Coordinate4D


class FCFSABABid(ABABid):
    def __init__(self, battery: int, a: Coordinate4D, b: Coordinate4D, stay: int):
        super().__init__(battery, a, b, stay)
