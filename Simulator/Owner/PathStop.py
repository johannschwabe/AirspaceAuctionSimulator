import random
from typing import Optional, TYPE_CHECKING
from Simulator.Coordinate import Coordinate2D, Coordinate4D
from Simulator.Owner.StopType import StopType
from Simulator.Owner.Heatmap import Heatmap

if TYPE_CHECKING:
    from Simulator import Environment


class PathStop:
    def __init__(self, stop_type: str, position: Optional[Coordinate2D] = None, heatmap: Optional[Heatmap] = None):
        self.stop_type = stop_type
        self.position = position
        self.heatmap = heatmap

    def generate_coordinates(self, env: "Environment", t: int):
        if self.stop_type == StopType.RANDOM.value:
            dimensions = env.dimension
            coord = Coordinate4D(random.randint(0, dimensions.x - 1),
                                 env.min_height,
                                 random.randint(0, dimensions.z - 1),
                                 t)
        elif self.stop_type == StopType.POSITION.value:
            coord = Coordinate4D(self.position.x, env.min_height, self.position.z, t)

        elif self.stop_type == StopType.HEATMAP.value:
            winner = self.heatmap.generate_coordinate()
            coord = Coordinate4D(winner.x, env.min_height, winner.z, t)
        else:
            raise Exception("invalid stop type:", self)
        return coord
