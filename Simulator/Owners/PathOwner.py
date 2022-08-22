from abc import ABC
from typing import List, TYPE_CHECKING

from ..Agents.AllocationType import AllocationType
from ..Owners.Owner import Owner

if TYPE_CHECKING:
    from ..Owners.Location.GridLocation import GridLocation
    from ..Environment import Environment
    from ..Coordinates.Coordinate4D import Coordinate4D


class PathOwner(Owner, ABC):
    allocation_type: str = AllocationType.PATH.value

    def __init__(self, owner_id: int, name: str, color: str, stops: List["GridLocation"]):
        super().__init__(owner_id, name, color)
        self.stops = stops

    @staticmethod
    def generate_stop_coordinate(stop: "GridLocation", env: "Environment", t: int, near_radius: int,
                                 speed: int) -> "Coordinate4D":
        coord = stop.generate_coordinates(env, t)
        initial_y = coord.y

        while env.is_blocked_forever(coord, near_radius, speed):
            coord.y += 1
            if coord.y >= env.dimension.y:
                coord.y = env.min_height
            elif coord.y == initial_y:
                print("BLOCKED")
                break

        return coord
