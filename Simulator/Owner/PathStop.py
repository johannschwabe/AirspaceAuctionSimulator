from typing import Optional, Dict, List
from Simulator.Coordinate import Coordinate2D
from Simulator.Owner.Heatmap import Heatmap


class PathStop:
    def __init__(self, stop_type: str, position: Optional[Coordinate2D] = None, heatmap: Optional[Heatmap] = None):
        self.type = stop_type
        self.position = position
        self.heatmap = heatmap
