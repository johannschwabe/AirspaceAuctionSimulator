from typing import List, Optional

from .. Time import Tick
from ..Agent import Agent
from ..Bid import Bid, StationaryBid
from ..Coordinate import Coordinate, TimeCoordinate


class StationaryAgent(Agent):
    id: int = 0

    def __init__(
        self,
        block: List[Coordinate],
        start_t: Tick,
        end_t: Tick,
    ):
        super().__init__(near_border=[], far_border=[])

        self.block: List[Coordinate] = block
        self.start_t: Tick = start_t
        self.end_t: Tick = end_t

    def value_for_paths(self, paths: List[List[TimeCoordinate]]) -> float:
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

    def get_bid(self) -> Bid:
        return StationaryBid(self.battery, self.block, self.start_t, self.end_t)

    def clone(self):
        return StationaryAgent(self.block, self.start_t, self.end_t)

