from typing import TYPE_CHECKING

from . import ABBid

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D


class ABABid(ABBid):
    def __init__(self, battery: int, a: "Coordinate4D", b: "Coordinate4D", stay: int):
        super().__init__(battery, a, b)

        self.battery: int = battery
        self.stay: int = stay

        a2: "Coordinate4D" = a.clone()
        a2.t = b.t + b.t - a.t
        self.a2 = a2
