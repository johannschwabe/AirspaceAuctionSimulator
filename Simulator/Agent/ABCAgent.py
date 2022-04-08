from typing import List, Optional

from ..Agent import Agent
from ..Bid import Bid, ABCBid
from ..Coordinate import TimeCoordinate


class ABCAgent(Agent):
    def __init__(
        self,
        locations: List[TimeCoordinate],
        stays: List[int],
        speed: Optional[int] = None,
        battery: Optional[int] = None,
    ):
        super().__init__(speed=speed, battery=battery)

        self._locations: List[TimeCoordinate] = locations
        self.stays: List[int] = stays

    def value_for_paths(self, paths: List[List[TimeCoordinate]]) -> float:
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

    def get_bid(self) -> Bid:
        return ABCBid(self.battery, self._locations, self.stays)

    def clone(self):
        clone = ABCAgent(self._locations, self.stays, self.speed, self.battery)
        clone.id = self.id
        clone.is_clone = True
        Agent.id -= 1

        return clone
