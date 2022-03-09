from typing import List

from ..Time import Tick
from ..Bid import Bid
from ..Coordinate import Coordinate


class BlockerBid(Bid):
    def __init__(self, battery: int, block: List[Coordinate], start_t: Tick, end_t: Tick):
        super().__init__(battery)
        self.block: List[Coordinate] = block
        self.start_t: Tick = start_t
        self.end_t: Tick = end_t