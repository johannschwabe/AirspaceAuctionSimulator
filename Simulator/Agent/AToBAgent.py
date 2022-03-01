from typing import List, Optional

from ..Agent import Agent
from ..Bid import AToBBid, Bid
from ..Coordinate import Coordinate, TimeCoordinate


class AToBAgent(Agent):
    id: int = 0

    def __init__(
        self,
        a: TimeCoordinate,
        b: TimeCoordinate,
        speed: int = 1,
        battery: int = 20,
        near_border: Optional[List[Coordinate]] = None,
        far_border: Optional[List[Coordinate]] = None,
    ):
        super().__init__(speed=speed, battery=battery, near_border=near_border, far_border=far_border)

        self.a: TimeCoordinate = a
        self.b: TimeCoordinate = b

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
        return AToBBid(self.battery, self.a, self.b)

    def clone(self):
        return AToBAgent(self.a, self.b, self.speed, self.battery, self.near_border, self.far_boarder)

