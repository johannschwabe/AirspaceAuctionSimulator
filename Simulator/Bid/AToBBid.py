from ..Bid import Bid
from ..Coordinate import TimeCoordinate


class AToBBid(Bid):
    def __init__(self, battery: int, a: TimeCoordinate, b: TimeCoordinate):
        super().__init__(battery)
        self.a: TimeCoordinate = a
        self.b: TimeCoordinate = b
