from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

from ..Bid import Bid
from ..Coordinate import Coordinate, TimeCoordinate
from ..IO import Stringify
from ..helpers.Hit import Hit


class Agent(ABC, Stringify):
    id: int = 0

    default_near_border: List[Coordinate] = [Coordinate(x, y, z) for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2) ] # To dam big
    default_far_border: List[Coordinate] = [Coordinate(x, y, z) for x in range(-2, 3) for y in range(-2, 3) for z in range(-2, 3) ] # To dam big
    default_battery = 100000
    default_speed = 1

    def __init__(
        self,
        speed: Optional[int] = None,
        battery: Optional[int] = None,
        near_border: Optional[List[Coordinate]] = None,
        far_border: Optional[List[Coordinate]] = None,
    ):
        self.id = Agent.id
        Agent.id += 1
        self.is_clone = False

        self.speed: int = speed if speed is not None else Agent.default_speed
        self.battery: int = battery if battery is not None else Agent.default_battery

        # self._near_border: List[Coordinate] = near_border if near_border is not None else Agent.default_near_border
        # self._far_border: List[Coordinate] = far_border if far_border is not None else Agent.default_far_border

        self._allocated_paths: List[List["TimeCoordinate"]] = []

        self._allocated_coords: List["TimeCoordinate"] = []

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

    # def contains_coordinate(self, path: List[TimeCoordinate], coordinate: TimeCoordinate) -> Hit:
    #     current_position: Optional[Coordinate] = None
    #     for position in path:
    #         if position.t == coordinate.t:
    #             current_position = position
    #
    #     if current_position is None:
    #         return Hit.NO
    #
    #     if current_position == coordinate:
    #         return Hit.EXACT
    #
    #     far_hit: bool = False
    #     for relative_coordinate in self._far_border:
    #         absolut_coordinate = relative_coordinate + current_position
    #         if absolut_coordinate == relative_coordinate:
    #             far_hit = True
    #             break
    #
    #     if not far_hit:
    #         return Hit.NO
    #
    #     for relative_coordinate in self._near_border:
    #         absolut_coordinate = relative_coordinate + current_position
    #         if absolut_coordinate == relative_coordinate:
    #             return Hit.NEAR
    #
    #     return Hit.FAR

    def __repr__(self):
        return str(self.id)

