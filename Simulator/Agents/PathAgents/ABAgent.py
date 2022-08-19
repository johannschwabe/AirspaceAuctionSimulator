from abc import ABC
from typing import List, Optional, TYPE_CHECKING

from Simulator.Agents.AgentType import AgentType
from .PathAgent import PathAgent

if TYPE_CHECKING:
    from Simulator.Coordinates.Coordinate4D import Coordinate4D
    from Simulator.Path.PathSegment import PathSegment
    from Simulator.Simulator import Simulator


class ABAgent(PathAgent, ABC):
    agent_type: str = AgentType.AB.value

    def __init__(self,
                 a: "Coordinate4D",
                 b: "Coordinate4D",
                 simulator: "Simulator",
                 agent_id: Optional[int] = None,
                 speed: Optional[int] = None,
                 battery: Optional[int] = None,
                 near_radius: Optional[int] = None,
                 far_radius: Optional[int] = None):

        super().__init__(simulator,
                         agent_id=agent_id,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius,
                         far_radius=far_radius)

        self.a: "Coordinate4D" = a
        self.b: "Coordinate4D" = b

    def value_for_segments(self, path_segments: List["PathSegment"]) -> float:
        if len(path_segments) != 1:
            return 0.

        path_segment = path_segments[0]

        if len(path_segment.coordinates) == 0:
            return 0.

        start: Coordinate4D = path_segment.min
        destination: Coordinate4D = path_segment.max
        time = destination.t - start.t
        if time > self.battery:
            return -1.

        delay = destination.t - self.b.t
        if delay > 0:
            return round(max(0., 1. - delay / 100), 2)

        return 1.
