from . import ABBid
from ..Coordinates import Coordinate4D


class ABABid(ABBid):
    def __init__(self, battery: int, a: Coordinate4D, b: Coordinate4D, stay: int):
        super().__init__(battery, a, b)
        self.stay: int = stay
        self.a2 = a.clone()
        self.a2.t = b.t + b.t - a.t
