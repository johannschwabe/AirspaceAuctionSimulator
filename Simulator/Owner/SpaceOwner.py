from abc import ABC
import random
from typing import List, TYPE_CHECKING

from Simulator.Owner.Owner import Owner
from Simulator.Owner import StopType

if TYPE_CHECKING:
    from Simulator.Owner import PathStop
    from Simulator import Environment
    from Simulator.Coordinate import Coordinate4D

class SpaceOwner(Owner, ABC):
    def __init__(self, name: str, color: str, stops: List["PathStop"]):
        super().__init__(name, color)
        self.stops = stops

    @staticmethod
    def generate_stop_coordinates(stop: "PathStop", env: "Environment", t: int, dimension: "Coordinate4D"):
        if stop.stop_type == StopType.RANDOM.value:
            dimensions = env.dimension
            coord = Coordinate4D(random.randint(0, dimensions.x - 1),
                                 env.min_height,
                                 random.randint(0, dimensions.z - 1),
                                 t)
        elif stop.stop_type == StopType.POSITION.value:
            coord = Coordinate4D(stop.position.x, env.min_height, stop.position.z, t)

        elif stop.stop_type == StopType.HEATMAP.value:
            winner = stop.heatmap.generate_coordinate()
            coord = Coordinate4D(winner.x, env.min_height, winner.z, t)
        else:
            raise Exception("invalid stop type:", stop)
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
