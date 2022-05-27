from typing import List, TYPE_CHECKING

from . import Agent
from . import SpaceAgent
from ..Path import SpaceSegment
from ..Time import Tick
from ..Bid import Bid, StationaryBid
from ..Coordinate import Coordinate

if TYPE_CHECKING:
    from .. import Tick

class StationaryAgent(SpaceAgent):
    def __init__(
        self,
        block: List[Coordinate],
        start_t: Tick,
        end_t: Tick,
    ):
        super().__init__()

        self.block: List[Coordinate] = block
        self.start_t: Tick = start_t
        self.end_t: Tick = end_t

    def value_for_segments(self, paths: List[SpaceSegment]) -> float:
        if len(paths) == 0:
            return 0.

        value: float = 1.

        value -= (len(paths) - 1) / 100

        time: int = 0
        for path in paths:
            if len(path) > 0:
                time += path[-1].t - path[0].t

        value -= (self.end_t - self.start_t - time) / 100

        return round(value, 2)

    def get_bid(self, t: "Tick") -> Bid:
        return StationaryBid(self.battery, self.block, self.start_t, self.end_t)

    def clone(self):
        clone = StationaryAgent(self.block, self.start_t, self.end_t)
        clone.set_allocated_segments([segment.clone() for segment in self.get_allocated_segments()])
        clone.id = self.id
        clone.is_clone = True
        Agent._id -= 1

        return clone
