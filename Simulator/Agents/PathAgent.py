from abc import ABC
from typing import Optional, TYPE_CHECKING, List

from ..Agents.Agent import Agent
from ..Agents.AgentType import AgentType

if TYPE_CHECKING:
    from ..Segments.PathSegment import PathSegment
    from ..Simulator import Simulator
    from ..Coordinates.Coordinate4D import Coordinate4D


class PathAgent(Agent, ABC):
    DEFAULT_NEAR_RADIUS = 1
    DEFAULT_SPEED = 1
    DEFAULT_BATTERY = 100_000

    agent_type: str = AgentType.PATH.value

    def __init__(self,
                 locations: List["Coordinate4D"],
                 stays: List[int],
                 simulator: "Simulator",
                 agent_id: Optional[int] = None,
                 speed: Optional[int] = None,
                 battery: Optional[int] = None,
                 near_radius: Optional[int] = None):

        super().__init__(simulator, agent_id)

        self.locations: List["Coordinate4D"] = locations
        self.stays: List[int] = stays

        self.speed: int = speed if speed is not None else self.DEFAULT_SPEED
        self.battery: int = battery if battery is not None else self.DEFAULT_BATTERY
        self.near_radius = near_radius if near_radius is not None else self.DEFAULT_NEAR_RADIUS

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

    def does_collide(self, other_coordinate: "Coordinate4D", other_agent: "PathAgent"):
        for coordinate in self.get_allocated_coords():
            if other_coordinate.t <= coordinate.t <= other_coordinate.t + other_agent.speed:
                distance = coordinate.inter_temporal_distance(other_coordinate)
                if distance == 0:
                    return True
                if distance < self.near_radius or distance < other_agent.near_radius:
                    return True
        return False

    def value_for_segments(self, paths: List["PathSegment"]) -> float:
        if len(paths) == 0:
            return 0.

        if len(paths) != len(self.locations) - 1:
            print("Invalid allocation!!")
            return 0.

        value = 1.
        time = 0
        for path, location in zip(paths, self.locations[1:]):
            destination = path.max
            if not destination.inter_temporal_equal(location):
                print("Invalid allocation!")
                return 0.

            time += destination.t - path.min.t
            value -= (destination.t - location.t) / 100

        if time > self.battery:
            return -1.

        return round(max(0., value), 2)
