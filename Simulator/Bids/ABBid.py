from typing import TYPE_CHECKING

from .Bid import Bid

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D


class ABBid(Bid):
    def __init__(self, battery: int, a: "Coordinate4D", b: "Coordinate4D"):
        super().__init__(battery)

        self.battery: int = battery
        self.a: "Coordinate4D" = a
        self.b: "Coordinate4D" = b
