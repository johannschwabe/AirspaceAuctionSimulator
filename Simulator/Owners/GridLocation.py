import random
from typing import Optional, TYPE_CHECKING

from .GridLocationType import GridLocationType
from .Heatmap import Heatmap
from ..Coordinates.Coordinate2D import Coordinate2D
from ..Coordinates.Coordinate4D import Coordinate4D

if TYPE_CHECKING:
    from ..Environment.Environment import Environment


class GridLocation:
    def __init__(self, stop_type: str, position: Optional[Coordinate2D] = None, heatmap: Optional[Heatmap] = None):
        self.stop_type = stop_type
        self.position = position
        self.heatmap = heatmap

    def generate_coordinates(self, env: "Environment", t: int):
        if self.stop_type == GridLocationType.RANDOM.value:
            dimensions = env.dimension
            coord = Coordinate4D(random.randint(0, dimensions.x - 1),
                                 env.min_height,
                                 random.randint(0, dimensions.z - 1),
                                 t)
        elif self.stop_type == GridLocationType.POSITION.value:
            coord = Coordinate4D(self.position.x, env.min_height, self.position.z, t)

        elif self.stop_type == GridLocationType.HEATMAP.value:
            winner = self.heatmap.generate_coordinate()
            coord = Coordinate4D(winner.x, env.min_height, winner.z, t)
        else:
            raise Exception("invalid stop type:", self)
        return coord
