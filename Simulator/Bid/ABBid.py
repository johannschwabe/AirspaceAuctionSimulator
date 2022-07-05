from ..Bid import Bid
from ..Coordinate import Coordinate4D


class ABBid(Bid):
    def __init__(self, battery: int, a: Coordinate4D, b: Coordinate4D):
        super().__init__(battery)
        self.a: Coordinate4D = a
        self.b: Coordinate4D = b
