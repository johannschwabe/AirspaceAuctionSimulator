from typing import List, Optional, TYPE_CHECKING

from . import Agent, ABAgent
from .AgentType import AgentType
from ..Bid import Bid, ABABid
from ..Coordinate import Coordinate4D
from ..Path import PathSegment


class ABAAgent(ABAgent):
    agent_type: str = AgentType.ABA.value

    def __init__(
        self,
        a: Coordinate4D,
        b: Coordinate4D,
        stay: int = 5,
        speed: Optional[int] = None,
        battery: Optional[int] = None,
        near_radius: Optional[int | float] = None,
    ):
        super().__init__(a, b, speed=speed, battery=battery, near_radius=near_radius)

        self.stay: int = stay

    def value_for_segments(self, path_segments: List[PathSegment]) -> float:
        if len(path_segments) != 2:
            return 0.

        ab_path = path_segments[0]
        ba_path = path_segments[1]

        if len(ab_path) == 0 or len(ba_path) == 0:
            return 0.

        time = ab_path[-1].t - ab_path[0].t + ba_path[-1].t - ba_path[0].t
        if time > self.battery:
            return -1.

        delay = ab_path[-1].t - self.b.t
        if delay > 0:
            return round(max(0., 1. - delay / 100), 2)

        return 1.

    def get_bid(self, t: int) -> Bid:
        return ABABid(self.battery, self.a, self.b, self.stay)

    def clone(self):
        clone = ABAAgent(self.a, self.b, self.stay, self.speed, self.battery)
        clone.set_allocated_segments([segment.clone() for segment in self.get_allocated_segments()])
        clone.id = self.id
        clone.is_clone = True
        Agent._id -= 1

        return clone
