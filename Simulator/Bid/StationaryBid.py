from typing import List
from ..Bid import Bid
from ..Coordinate import Coordinate3D


class StationaryBid(Bid):
    def __init__(self, block: List[Coordinate3D], start_t: int, end_t: int):
        super().__init__(-1)
        self.block: List[Coordinate3D] = block
        self.start_t: int = start_t
        self.end_t: int = end_t
