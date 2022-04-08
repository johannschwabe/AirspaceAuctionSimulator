from abc import ABC, abstractmethod
from typing import List, Optional

from ..Bid import Bid
from ..Coordinate import TimeCoordinate
from ..IO import Stringify


class Agent(ABC, Stringify):
    id: int = 0
    max_near_field_radius = 2
    max_far_field_radius = 4
    default_bubble = [-1, -1, -1, +1, +1, +1]

    default_battery = 100000
    default_speed = 1

    def __init__(
        self,
        speed: Optional[int] = None,
        battery: Optional[int] = None,
    ):
        self.id = Agent.id
        Agent.id += 1
        self.is_clone = False

        self.speed: int = speed if speed is not None else Agent.default_speed
        self.battery: int = battery if battery is not None else Agent.default_battery

        self._allocated_paths: List[List["TimeCoordinate"]] = []

        self._allocated_coords: List["TimeCoordinate"] = []

        self.bubble = Agent.default_bubble

        self.near_radius = 1
        self.far_radius = 3

        self.optimal_welfare: float = 1.
        self.costs: float = 0.
        self.flight_time: int = 0

    def as_dict(self, ignore_keys=tuple([]), date_format="%Y-%m-%d") -> dict:
        selfDict = self.__dict__
        selfDict["locations"] = self.locations
        selfDict["achieved_welfare"] = self.achieved_welfare
        return Stringify.to_dict(self, ignore_keys=ignore_keys, date_format=date_format, stop_recursion=True)

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

    def get_allocated_coords(self) -> List["TimeCoordinate"]:
        return self._allocated_coords

    def add_allocated_path(self, path: List[TimeCoordinate]):
        self._allocated_paths.append(path)

    def add_allocated_coord(self, coord: "TimeCoordinate"):
        if coord not in self._allocated_coords:
            self._allocated_coords.append(coord)

    def get_allocated_value(self):
        return self.value_for_paths(self._allocated_paths)

    def get_allocated_paths(self):
        return self._allocated_paths

    def __repr__(self):
        return str(self.id)
