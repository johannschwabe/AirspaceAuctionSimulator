from typing import List, Optional

from . import AToBAgent
from ..Bid import AToBBid, Bid, AToBToABid
from ..Coordinate import Coordinate, TimeCoordinate


class AToBToAAgent(AToBAgent):
    id: int = 0

    def __init__(
        self,
        a: TimeCoordinate,
        b: TimeCoordinate,
        stay: int = 2,
        speed: int = 1,
        battery: int = 20,
        near_border: Optional[List[Coordinate]] = None,
        far_border: Optional[List[Coordinate]] = None,
    ):
        super().__init__(a, b, speed=speed, battery=battery, near_border=near_border, far_border=far_border)
        self.stay: int = stay

    def value_for_path(self, path: List[TimeCoordinate]) -> float:
        if len(path) == 0:
            return 0.

        start: TimeCoordinate = path[0]
        destination: TimeCoordinate = path[-1]
        time = destination.t - start.t
        if time > self.battery:
            return 0.

        delay = destination.t - self.b.t
        if delay > 0:
            return max(0., 1. - delay / 100)

        return 1.

    def get_bid(self) -> Bid:
        return AToBToABid(self.battery, self.a, self.b, self.stay)

    def clone(self):
        return AToBAgent(self.a, self.b, self.speed, self.battery, self.near_border, self.far_boarder)

