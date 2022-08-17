from abc import ABC
from typing import List, TYPE_CHECKING

from AAS.Agent.AllocationType import AllocationType
from AAS.Owner import Owner

if TYPE_CHECKING:
    from AAS.Owner import GridLocation
    from AAS import Environment


class PathOwner(Owner, ABC):
    allocation_type: str = AllocationType.PATH.value

    def __init__(self, name: str, color: str, stops: List["GridLocation"]):
        super().__init__(name, color)
        self.stops = stops

    @staticmethod
    def generate_stop_coordinate(stop: "GridLocation", env: "Environment", t: int, near_radius: int, speed: int):
        coord = stop.generate_coordinates(env, t)

        while env.is_blocked_forever(coord, near_radius, speed):
            coord.y += 1
            if coord.y >= env.get_dim().y:
                coord.y = env.min_height
                print("BLOCKED")
                break

        return coord
