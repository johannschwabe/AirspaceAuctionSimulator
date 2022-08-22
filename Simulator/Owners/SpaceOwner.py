from abc import ABC
from typing import List, TYPE_CHECKING

from .Owner import Owner
from ..Agents.AllocationType import AllocationType

if TYPE_CHECKING:
    from ..Owners.Location.GridLocation import GridLocation
    from ..Environment.Environment import Environment
    from ..Coordinates.Coordinate4D import Coordinate4D


class SpaceOwner(Owner, ABC):
    allocation_type: str = AllocationType.SPACE.value

    def __init__(self, owner_id: int, name: str, color: str, stops: List["GridLocation"]):
        super().__init__(owner_id, name, color)
        self.stops = stops

    @staticmethod
    def generate_stop_coordinates(stop: "GridLocation", env: "Environment", t: int) -> "Coordinate4D":
        coord = stop.generate_coordinates(env, t)
        return coord
