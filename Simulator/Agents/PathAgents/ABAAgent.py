from abc import ABC
from typing import List, Optional, TYPE_CHECKING

from .ABAgent import ABAgent
from ..AgentType import AgentType

if TYPE_CHECKING:
    from ...Coordinates.Coordinate4D import Coordinate4D
    from ...Allocation.PathSegment import PathSegment
    from ...Simulator import Simulator


class ABAAgent(ABAgent, ABC):
    agent_type: str = AgentType.ABA.value

    def __init__(self,
                 a: "Coordinate4D",
                 b: "Coordinate4D",
                 stay: int,
                 simulator: "Simulator",
                 agent_id: Optional[int] = None,
                 speed: Optional[int] = None,
                 battery: Optional[int] = None,
                 near_radius: Optional[int] = None):

        super().__init__(a,
                         b,
                         simulator,
                         agent_id=agent_id,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius)

        self.stay: int = stay

    def value_for_segments(self, path_segments: List["PathSegment"]) -> float:
        if len(path_segments) != 2:
            return 0.

        ab_path = path_segments[0]
        ba_path = path_segments[1]

        if len(ab_path.coordinates) == 0 or len(ba_path.coordinates) == 0:
            return 0.

        time = ab_path.max.t - ab_path.min.t + ba_path.max.t - ba_path.min.t
        if time > self.battery:
            return -1.

        delay = ab_path.max.t - self.b.t
        if delay > 0:
            return round(max(0., 1. - delay / 100), 2)

        return 1.
