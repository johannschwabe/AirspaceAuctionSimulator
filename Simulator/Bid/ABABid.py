from . import ABBid
from ..Coordinate import TimeCoordinate


class ABABid(ABBid):
    def __init__(self, battery: int, a: TimeCoordinate, b: TimeCoordinate, stay: int):
        super().__init__(battery, a, b)
        self.stay: int = stay
        self.a2 = a.clone()
        self.a2.t = b.t + b.t - a.t
