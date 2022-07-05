from typing import Optional, Dict, List
from Simulator.Coordinate import Coordinate2D


class PathStop:
    def __init__(self, stopType: str, position: Optional[Coordinate2D] = None, heatmap: Optional[Dict[float, List[Coordinate2D]]] = None):
        self.type: str = stopType
        self.position: Optional[Coordinate2D] = position
        self.heatmap: Optional[Dict[float, List[Coordinate2D]]] = heatmap
