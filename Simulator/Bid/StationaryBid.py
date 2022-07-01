from typing import List, TYPE_CHECKING

from ..Bid import Bid
if TYPE_CHECKING:
    from ..Coordinate import TimeCoordinate


class StationaryBid(Bid):
    def __init__(self, blocks: List[List["TimeCoordinate"]]):
        super().__init__(-1)
        self.blocks: List[List["TimeCoordinate"]] = blocks

