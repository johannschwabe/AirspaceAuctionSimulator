from typing import List, TYPE_CHECKING

from ..Bid import Bid
if TYPE_CHECKING:
    from ..Coordinates import Coordinate4D


class StationaryBid(Bid):
    def __init__(self, blocks: List[List["Coordinate4D"]]):
        super().__init__(-1)
        self.blocks: List[List["Coordinate4D"]] = blocks

