from typing import Optional
from Simulator.Coordinate import Coordinate2D
from Simulator.Owner import StopType
from Simulator.Owner.Heatmap import Heatmap


class PathStop:
    def __init__(self, stop_type: str, position: Optional[Coordinate2D] = None, heatmap: Optional[Heatmap] = None):
        self.stop_type = stop_type
        self.position = position
        self.heatmap = heatmap
