from AAS import StationaryBid, Coordinate4D


class FCFSStationaryBid(StationaryBid):
    def __init__(self, blocks: List[List[Coordinate4D]]):
        super().__init__(blocks)
