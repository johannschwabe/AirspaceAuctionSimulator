from typing import List, Optional, TYPE_CHECKING

from . import Agent
from .PathAgent import PathAgent
from ..Bid import ABBid, Bid
from ..Coordinate import TimeCoordinate
from ..Path import PathSegment

if TYPE_CHECKING:
    from .. import Tick

class ABAgent(PathAgent):
    def __init__(
        self,
        a: TimeCoordinate,
        b: TimeCoordinate,
        speed: Optional[int] = None,
        battery: Optional[int] = None,
        near_radius: Optional[int] = None
    ):
        super().__init__(speed, battery, near_radius)

        self.a: TimeCoordinate = a
        self.b: TimeCoordinate = b

    def value_for_segments(self, path_segments: List[PathSegment]) -> float:
        if len(path_segments) != 1:
            return 0.

        path_segment = path_segments[0]

        if len(path_segment) == 0:
            return 0.

        start: TimeCoordinate = path_segment[0]
        destination: TimeCoordinate = path_segment[-1]
        time = destination.t - start.t
        if time > self.battery:
            return -1.

        delay = destination.t - self.b.t
        if delay > 0:
            return round(max(0., 1. - delay / 100), 2)

        return 1.

    def get_bid(self, t: "Tick") -> Bid:
        return ABBid(self.battery, self.a, self.b)

    def clone(self):
        clone = ABAgent(self.a, self.b, self.speed, self.battery)
        clone.id = self.id
        clone.set_allocated_segments([segment.clone() for segment in self.get_allocated_segments()])
        clone.is_clone = True
        Agent._id -= 1
        return clone
