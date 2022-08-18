from abc import ABC
from typing import List, TYPE_CHECKING

from AAS.Agent.AllocationType import AllocationType
from AAS.Owners import Owner

if TYPE_CHECKING:
    from AAS.Owners import GridLocation
    from AAS import Environment
    from AAS.Coordinates import Coordinate4D


class SpaceOwner(Owner, ABC):
    allocation_type: str = AllocationType.SPACE.value

    def __init__(self, name: str, color: str, stops: List["GridLocation"]):
        super().__init__(name, color)
        self.stops = stops

    @staticmethod
    def generate_stop_coordinates(stop: "GridLocation", env: "Environment", t: int, dimension: "Coordinate4D"):
        coord = stop.generate_coordinates(env, t)
        top_right = coord + dimension

        while len(list(env.intersect_box(coord, top_right, False))):
            coord.y += 1
            top_right.y += 1
            if coord.y >= env.get_dim().y:
                coord.y = env.min_height
                top_right.y = env.min_height
                print("BLOCKED")
                break
        return coord