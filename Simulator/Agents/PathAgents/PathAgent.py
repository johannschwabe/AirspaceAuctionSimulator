from abc import ABC
from typing import Optional, TYPE_CHECKING, List

from Simulator.Agents.Agent import Agent
from Simulator.Agents.AllocationType import AllocationType

if TYPE_CHECKING:
    from Simulator.Path.PathSegment import PathSegment
    from Simulator.Simulator import Simulator
    from Simulator.Coordinates.Coordinate4D import Coordinate4D


class PathAgent(Agent, ABC):
    DEFAULT_NEAR_RADIUS = 1
    DEFAULT_FAR_RADIUS = 2
    DEFAULT_SPEED = 1
    DEFAULT_BATTERY = 100_000

    allocation_type: str = AllocationType.PATH.value

    def __init__(self,
                 simulator: "Simulator",
                 agent_id: Optional[int] = None,
                 speed: Optional[int] = None,
                 battery: Optional[int] = None,
                 near_radius: Optional[int] = None,
                 far_radius: Optional[int] = None):

        super().__init__(simulator, agent_id)

        self.speed: int = speed if speed is not None else self.DEFAULT_SPEED
        self.battery: int = battery if battery is not None else self.DEFAULT_BATTERY
        self.near_radius = near_radius if near_radius is not None else self.DEFAULT_NEAR_RADIUS
        self.far_radius = far_radius if far_radius is not None else self.DEFAULT_FAR_RADIUS

        self.allocated_segments: List["PathSegment"] = []

    def get_airtime(self) -> int:
        airtime = 0
        for path_segment in self.allocated_segments:
            airtime += path_segment.max.t - path_segment.min.t
        return airtime

    def add_allocated_segment(self, path_segment: "PathSegment"):
        if len(self.allocated_segments) > 0 and self.allocated_segments[-1].same(path_segment):
            self.allocated_segments[-1].join(path_segment)
        else:
            self.allocated_segments.append(path_segment)

    def get_allocated_coords(self) -> List["Coordinate4D"]:
        return [coord for path_segment in self.allocated_segments for coord in path_segment.coordinates]
