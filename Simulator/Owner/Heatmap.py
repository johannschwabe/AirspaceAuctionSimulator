import random
from typing import Dict, List, Optional

from Simulator.Coordinate import Coordinate2D
from Simulator.Owner.HeatmapType import HeatmapType


class Heatmap:
    def __init__(self,
                 heatmap_type: str,
                 inverse_sparse: Optional[Dict[float, List[Coordinate2D]]] = None,
                 sparse: Optional[Dict[Coordinate2D, float]] = None,
                 matrix: Optional[List[List[float]]] = None,
                 ):
        self.type = heatmap_type
        self.inverse_sparse = inverse_sparse
        self.sparse = sparse
        self.matrix = matrix

    def generate_coordinate(self):
        tombola: List[Coordinate2D] = []
        if self.type == HeatmapType.INVERSE_SPARSE.value:
            for item in self.inverse_sparse.items():
                for i in range(0, int(item[0] * 10)):
                    tombola.extend(item[1])
        elif self.type == HeatmapType.SPARSE.value:
            for item in self.sparse.items():
                for i in range(0, int(item[1] * 10)):
                    tombola.append(item[0])
        elif self.type == HeatmapType.MATRIX.value:
            for x, row in enumerate(self.matrix):
                for z, val in enumerate(row):
                    if val > 0:
                        for i in range(0, int(val * 10)):
                            tombola.append(Coordinate2D(x, z))
        return random.choice(tombola)
