from typing import List

from .Agent import Agent
from .SpaceAgent import SpaceAgent
from ..Coordinate import Coordinate3D
from ..Path import SpaceSegment
from ..Bid import Bid, StationaryBid


class StationaryAgent(SpaceAgent):
    def __init__(
        self,
        block: List[Coordinate3D],
        start_t: int,
        end_t: int,
    ):
        super().__init__()

        self.block: List[Coordinate3D] = block
        self.start_t: int = start_t
        self.end_t: int = end_t

    def value_for_segments(self, space: List[SpaceSegment]) -> float:
        if len(space) == 0:
            return 0.

        value: float = 1.

        value -= (len(space) - 1) / 100

        time: int = 0

        value -= (self.end_t - self.start_t - time) / 100

        return round(value, 2)

    def get_bid(self, t: int) -> Bid:
        return StationaryBid(self.block, self.start_t, self.end_t)

    def clone(self):
        clone = StationaryAgent(self.block, self.start_t, self.end_t)
        clone.set_allocated_segments([segment.clone() for segment in self.get_allocated_segments()])
        clone.id = self.id
        clone.is_clone = True
        Agent._id -= 1

        return clone
