import math
import random
from typing import Optional, TYPE_CHECKING

from Simulator import Coordinate2D, Coordinate4D
from .GridLocationType import GridLocationType
from .Heatmap import Heatmap

if TYPE_CHECKING:
    from Simulator import Environment


class GridLocation:
    def __init__(self,
                 grid_location_type: str,
                 position: Optional[Coordinate2D] = None,
                 heatmap: Optional[Heatmap] = None):
        self.grid_location_type = grid_location_type
        self.position = position
        self.heatmap = heatmap

    def generate_coordinates(self, env: "Environment", t: int):
        if self.grid_location_type == GridLocationType.RANDOM.value:
            dimensions = env.dimension
            coord = Coordinate4D(random.randint(0, math.floor(dimensions.x) - 1),
                                 env.min_height,
                                 random.randint(0, math.floor(dimensions.z) - 1),
                                 t)
        elif self.grid_location_type == GridLocationType.POSITION.value:
            coord = Coordinate4D(self.position.x, env.min_height, self.position.z, t)

        elif self.grid_location_type == GridLocationType.HEATMAP.value:
            winner = self.heatmap.generate_coordinate()
            coord = Coordinate4D(winner.x, env.min_height, winner.z, t)
        else:
            raise Exception("invalid stop type:", self)
        return coord
