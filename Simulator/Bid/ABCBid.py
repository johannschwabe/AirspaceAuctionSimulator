from typing import List

from . import Bid
from ..Coordinate import TimeCoordinate


class ABCBid(Bid):
    def __init__(self, battery: int, locations: List[TimeCoordinate], stays: List[int]):
        super().__init__(battery)
        self.locations = locations
        self.stays = stays

