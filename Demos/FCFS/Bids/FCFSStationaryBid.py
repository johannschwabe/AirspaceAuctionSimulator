from AAS import StationaryBid, Coordinate4D


class FCFSStationaryBid(StationaryBid):
    def __init__(self, blocks: list[list[Coordinate4D]]):
        super().__init__(blocks)
