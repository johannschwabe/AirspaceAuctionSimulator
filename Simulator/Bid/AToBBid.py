from ..Bid import Bid
from ..Coordinate import TimeCoordinate


class AToBBid(Bid):
    def __init__(self, a: TimeCoordinate, b: TimeCoordinate):
        super().__init__()
        self.a: TimeCoordinate = a
        self.b: TimeCoordinate = b
