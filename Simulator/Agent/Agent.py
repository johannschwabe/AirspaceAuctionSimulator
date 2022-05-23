from abc import ABC, abstractmethod
from typing import List, Optional

from .AgentType import AgentType
from ..Bid import Bid
from ..Coordinate import TimeCoordinate


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

        self._allocated_paths: List[List["TimeCoordinate"]] = []

        self._allocated_coords: List["TimeCoordinate"] = []

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
    def value_for_paths(self, paths: List[List[TimeCoordinate]]) -> float:
        pass

    @abstractmethod
    def get_bid(self) -> Bid:
        pass

    @abstractmethod
    def clone(self):
        pass

    def get_airtime(self) -> int:
        airtime = 0
        for path in self._allocated_paths:
            airtime += path[-1].t - path[0].t
        return airtime

    def get_allocated_coords(self) -> List["TimeCoordinate"]:
        return [y for x in self._allocated_paths for y in x]

    def add_allocated_paths(self, path: List["TimeCoordinate"]):
        self._allocated_paths.append(path)

    def get_allocated_paths(self):
        return self._allocated_paths

    def get_allocated_value(self):
        return self.value_for_paths(self._allocated_paths)

    def __repr__(self):
        return str(self.id)
