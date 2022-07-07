from abc import ABC
from typing import Optional, TYPE_CHECKING

from . import Agent
from .AllocationType import AllocationType

if TYPE_CHECKING:
    from ..Path import PathSegment


class PathAgent(Agent, ABC):
    default_near_radius = 1
    default_far_radius = 2
    default_speed = 1
    default_battery = 100000

    allocation_type: str = AllocationType.PATH.value

    def __init__(
        self,
        speed: Optional[int] = None,
        battery: Optional[int] = None,
        near_radius: Optional[int | float] = None,
    ):
        super().__init__()

        self.speed: int = speed if speed is not None else PathAgent.default_speed
        self.battery: int = battery if battery is not None else PathAgent.default_battery

        self.near_radius = near_radius if near_radius is not None else PathAgent.default_near_radius
        self.far_radius = PathAgent.default_far_radius
        self.flight_time: int = 0

    def get_airtime(self) -> int:
        airtime = 0
        for path_segment in self._allocated_segments:
            airtime += path_segment[-1].t - path_segment[0].t
        return airtime

    def add_allocated_segment(self, path_segment: "PathSegment"):
        if len(self._allocated_segments) > 0 and self._allocated_segments[-1].same(path_segment):
            self._allocated_segments[-1].join(path_segment)
        else:
            self._allocated_segments.append(path_segment)
