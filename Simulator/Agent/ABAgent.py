from typing import List, Optional

from . import Agent
from .AgentType import AgentType
from ..Bid import ABBid, Bid
from ..Coordinate import TimeCoordinate


class ABAgent(Agent):
    def __init__(
        self,
        a: TimeCoordinate,
        b: TimeCoordinate,
        speed: Optional[int] = None,
        battery: Optional[int] = None,
    ):
        super().__init__(AgentType.AB, speed=speed, battery=battery)

        self.a: TimeCoordinate = a
        self.b: TimeCoordinate = b

    def value_for_paths(self, paths: List[List[TimeCoordinate]]) -> float:
        if len(paths) != 1:
            return 0.

        path = paths[0]

        if len(path) == 0:
            return 0.

        start: TimeCoordinate = path[0]
        destination: TimeCoordinate = path[-1]
        time = destination.t - start.t
        if time > self.battery:
            return -1.

        delay = destination.t - self.b.t
        if delay > 0:
            return round(max(0., 1. - delay / 100), 2)

        return 1.

    def get_bid(self) -> Bid:
        return ABBid(self.battery, self.a, self.b)

    def clone(self):
        clone = ABAgent(self.a, self.b, self.speed, self.battery)
        clone.id = self.id
        clone.is_clone = True
        Agent._id -= 1
        return clone
