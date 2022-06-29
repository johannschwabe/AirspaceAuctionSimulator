from typing import List, Optional, TYPE_CHECKING

from . import Agent
from .PathAgent import PathAgent
from ..Bid import Bid, ABCBid
from ..Coordinate import TimeCoordinate
from ..Path import PathSegment

if TYPE_CHECKING:
    from .. import Tick


class ABCAgent(PathAgent):
    def __init__(
        self,
        locations: List[TimeCoordinate],
        stays: List[int],
        speed: Optional[int] = None,
        battery: Optional[int] = None,
    ):
        super().__init__(speed, battery)

        self._locations: List[TimeCoordinate] = locations
        self.stays: List[int] = stays

    def value_for_segments(self, paths: List[PathSegment]) -> float:
        if len(paths) == 0:
            return 0.

        if len(paths) != len(self._locations) - 1:
            print("Invalid allocation!")
            return 0.

        value = 1.
        time = 0
        for path, location in zip(paths, self._locations[1:]):
            destination = path[-1]
            if not destination.inter_temporal_equal(location):
                print("Invalid allocation!")
                return 0.

            time += destination.t - path[0].t
            value -= (destination.t - location.t) / 100

        if time > self.battery:
            return -1.

        return round(max(0., value), 2)

    def get_bid(self, t: "Tick") -> Bid:
        return ABCBid(self.battery, self._locations, self.stays)

    def clone(self):
        clone = ABCAgent(self._locations, self.stays, self.speed, self.battery)
        clone.set_allocated_segments([segment.clone() for segment in self.get_allocated_segments()])
        clone.id = self.id
        clone.is_clone = True
        Agent._id -= 1
        return clone
