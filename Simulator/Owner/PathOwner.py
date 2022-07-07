from abc import ABC
import random
from typing import List

from Simulator import Environment
from Simulator.Coordinate import Coordinate4D
from Simulator.Owner import Owner, PathStop
from Simulator.Owner.StopType import StopType


class PathOwner(Owner, ABC):
    def __init__(self, name: str, color: str, stops: List[PathStop]):
        super().__init__(name, color)
        self.stops = stops

    @staticmethod
    def generate_stop_coordinate(stop: PathStop, env: Environment, t: int, near_radius: int, speed: int):
        coord: Coordinate4D
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

        while env.is_blocked_forever(coord, near_radius, speed):
            coord.y += 1
            if coord.y >= env.get_dim().y:
                coord.y = env.min_height
                print("BLOCKED")
                break

        return coord
