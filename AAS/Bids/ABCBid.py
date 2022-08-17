from typing import List

from . import Bid
from ..Coordinates import Coordinate4D


class ABCBid(Bid):
    def __init__(self, battery: int, locations: List[Coordinate4D], stays: List[int]):
        super().__init__(battery)
        self.locations = locations
        self.stays = stays

