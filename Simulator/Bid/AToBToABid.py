from . import AToBBid
from ..Coordinate import TimeCoordinate


class AToBToABid(AToBBid):
    def __init__(self, battery: int, a: TimeCoordinate, b: TimeCoordinate, stay: int):
        super().__init__(battery, a, b)
        self.stay: int = stay

