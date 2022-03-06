from abc import ABC, abstractmethod
from typing import List, Optional

from ..Bid import Bid
from ..Coordinate import Coordinate, TimeCoordinate
from ..Field import Field
from ..helpers.Hit import Hit


class Agent(ABC):
    id: int = 0

    default_near_border: List[Coordinate] = [Coordinate(x, y, z) for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2)]
    default_far_border: List[Coordinate] = [Coordinate(x, y, z) for x in range(-2, 3) for y in range(-2, 3) for z in range(-2, 3)]
    default_battery = 100
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

        self.near_border: List[Coordinate] = near_border if near_border is not None else Agent.default_near_border
        self.far_boarder: List[Coordinate] = far_border if far_border is not None else Agent.default_far_border

        self.allocated_paths: List[List[TimeCoordinate]] = []

        self.allocated_fields: List[Field] = []
        self.allocated_near_fields: List[Field] = []
        self.allocated_far_fields: List[Field] = []


    @abstractmethod
    def value_for_paths(self, paths: List[List[TimeCoordinate]]) -> float:
        pass

    @abstractmethod
    def get_bid(self) -> Bid:
        pass

    @abstractmethod
    def clone(self):
        pass

    def get_near_coordinates(self, position: TimeCoordinate) -> List[TimeCoordinate]:
        return [TimeCoordinate(coordinate.x + position.x, coordinate.y + position.y, coordinate.z + position.z, position.t) for coordinate in self.near_border]

    def get_far_coordinates(self, position: TimeCoordinate) -> List[TimeCoordinate]:
        return [TimeCoordinate(coordinate.x + position.x, coordinate.y + position.y, coordinate.z + position.z, position.t) for coordinate in self.far_boarder]

    def contains_coordinate(self, path: List[TimeCoordinate], coordinate: TimeCoordinate) -> Hit:
        current_position: Optional[Coordinate] = None
        for position in path:
            if position.t == coordinate.t:
                current_position = position

        if current_position is None:
            return Hit.NO

        if current_position == coordinate:
            return Hit.EXACT

        far_hit: bool = False
        for relative_coordinate in self.far_boarder:
            absolut_coordinate = relative_coordinate + current_position
            if absolut_coordinate == relative_coordinate:
                far_hit = True
                break

        if not far_hit:
            return Hit.NO

        for relative_coordinate in self.near_border:
            absolut_coordinate = relative_coordinate + current_position
            if absolut_coordinate == relative_coordinate:
                return Hit.NEAR

        return Hit.FAR

    def __repr__(self):
        return str(self.id)
