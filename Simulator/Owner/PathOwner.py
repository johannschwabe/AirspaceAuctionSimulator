from abc import ABC
import random
from typing import List

from Simulator import Environment
from Simulator.Coordinate import Coordinate4D, Coordinate2D
from Simulator.Owner import PathStop
from Simulator.Owner.Owner import Owner


class PathOwner(Owner, ABC):
    def __init__(self, name: str, color: str, stops: List[PathStop]):
        super().__init__(name, color)
        self.stops = stops

    @staticmethod
    def generate_stop_coordinate(stop: PathStop, env: Environment, t: int, near_radius: int, speed: int):
        coord: Coordinate4D
        if stop.type == "random":
            dimensions = env.dimension
            coord = Coordinate4D(random.randint(0, dimensions.x - 1),
                                 env.min_height,
                                 random.randint(0, dimensions.z - 1),
                                 t)
        elif stop.type == "position":
            coord = Coordinate4D(stop.position.x, env.min_height, stop.position.z, t)
        elif stop.type == "heatmap":
            tombola: List[Coordinate2D] = []
            for key in stop.heatmap:
                for i in range(0, int(key * 10)):
                    tombola.extend(stop.heatmap[key])
            winner = random.choice(tombola)
            coord = Coordinate4D(winner.x, env.min_height, winner.z, t)
        else:
            raise Exception("invalid stop type:", stop)

        while env.is_blocked(coord, near_radius, speed):
            coord.y += 1
            if coord.y >= env.get_dim().y:
                coord.y = env.min_height
                break

        return coord
