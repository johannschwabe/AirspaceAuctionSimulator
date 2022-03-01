from typing import List, Optional

from . import ABAgent
from ..Bid import Bid, ABABid
from ..Coordinate import Coordinate, TimeCoordinate


class ABAAgent(ABAgent):
    id: int = 0

    def __init__(
        self,
        a: TimeCoordinate,
        b: TimeCoordinate,
        stay: int = 5,
        speed: int = 1,
        battery: int = 30,
        near_border: Optional[List[Coordinate]] = None,
        far_border: Optional[List[Coordinate]] = None,
    ):
        super().__init__(a, b, speed=speed, battery=battery, near_border=near_border, far_border=far_border)
        self.stay: int = stay

    def value_for_paths(self, paths: List[List[TimeCoordinate]]) -> float:
        if len(paths) != 2:
            return 0.

        ab_path = paths[0]
        ba_path = paths[1]

        if len(ab_path) == 0 or len(ba_path) == 0:
            return 0.

        time = ab_path[-1].t - ab_path[0].t + ba_path[-1].t - ba_path[0].t
        if time > self.battery:
            return -1.

        delay = ab_path[-1].t - self.b.t
        if delay > 0:
            return max(0., 1. - delay / 100)

        return 1.

    def get_bid(self) -> Bid:
        return ABABid(self.battery, self.a, self.b, self.stay)

    def clone(self):
        return ABAAgent(self.a, self.b, self.stay, self.speed, self.battery, self.near_border, self.far_boarder)

