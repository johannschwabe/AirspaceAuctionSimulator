from typing import List
from ..Bid import Bid


class StationaryBid(Bid):
    def __init__(self, block: List[Coordinate], start_t: int, end_t: int):
        super().__init__(-1)
        self.block: List[Coordinate] = block
        self.start_t: int = start_t
        self.end_t: int = end_t
