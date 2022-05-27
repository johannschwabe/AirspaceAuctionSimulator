from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

from .AgentType import AgentType
from ..Bid import Bid
from ..Coordinate import TimeCoordinate
from ..Path import PathSegment, SpaceSegment

if TYPE_CHECKING:
    from .. import Tick

class Agent(ABC):
    _id: int = 0
    max_near_field_radius = 2
    max_far_field_radius = 4
    default_near_radius = 1
    default_far_radius = 2

    default_battery = 100000
    default_speed = 1

    def __init__(
        self,
        agent_type: AgentType,
        speed: Optional[int] = None,
        battery: Optional[int] = None,
    ):
        self.id = Agent._id
        Agent._id += 1
        self.is_clone = False

        self.agent_type = agent_type

        self.speed: int = speed if speed is not None else Agent.default_speed
        self.battery: int = battery if battery is not None else Agent.default_battery

        self._allocated_paths: List[PathSegment] = []

        self.near_radius = Agent.default_near_radius
        self.far_radius = Agent.default_far_radius

        self.optimal_welfare: float = 1.
        self.costs: float = 0.
        self.flight_time: int = 0

    @property
    def locations(self) -> List[TimeCoordinate]:
        locations: List[TimeCoordinate] = []
        for path in self._allocated_paths:
            locations += path
        return locations

    @property
    def achieved_welfare(self) -> float:
        return self.value_for_paths(self._allocated_paths)

    @abstractmethod
    def value_for_paths(self, paths: List[PathSegment]) -> float:
        pass

    @abstractmethod
    def get_bid(self, t: "Tick") -> Bid:
        pass

    @abstractmethod
    def clone(self):
        pass

    def get_airtime(self) -> int:
        airtime = 0
        for path_segment in self._allocated_paths:
            airtime += path_segment.coordinates[-1].t - path_segment.coordinates[0].t
        return airtime

    def get_allocated_coords(self) -> List["TimeCoordinate"]:
        return [coord for path_segment in self._allocated_paths for coord in path_segment.coordinates]

    def add_allocated_path_segment(self, path_segment: PathSegment):
        if self._allocated_paths[-1].same(path_segment):
            self._allocated_paths[-1].join(path_segment)
        else:
            self._allocated_paths.append(path_segment)

    def get_allocated_paths(self) -> List["PathSegment"]:
        return self._allocated_paths

    def get_allocated_value(self) -> float:
        return self.value_for_paths(self._allocated_paths)

    def set_allocated_paths(self, paths: List["PathSegment"]):
        self._allocated_paths = paths

    def __repr__(self):
        return str(self.id)
