import random
from typing import Dict, List, Optional

from Simulator import Coordinate2D
from .HeatmapType import HeatmapType


class Heatmap:
    def __init__(self,
                 heatmap_type: str,
                 inverse_sparse: Optional[Dict[float, List[Coordinate2D]]] = None,
                 sparse: Optional[Dict[Coordinate2D, float]] = None,
                 matrix: Optional[List[List[float]]] = None,
                 ):
        self.heatmap_type = heatmap_type
        self.inverse_sparse = inverse_sparse
        self.sparse = sparse
        self.matrix = matrix

    def assemble_tombola(self) -> List[Coordinate2D]:
        tombola: List[Coordinate2D] = []
        if self.heatmap_type == HeatmapType.INVERSE_SPARSE.value:
            for item in self.inverse_sparse.items():
                for i in range(0, int(item[0] * 10)):
                    tombola.extend(item[1])
        elif self.heatmap_type == HeatmapType.SPARSE.value:
            for item in self.sparse.items():
                for i in range(0, int(item[1] * 10)):
                    tombola.append(item[0])
        elif self.heatmap_type == HeatmapType.MATRIX.value:
            for x, row in enumerate(self.matrix):
                for z, val in enumerate(row):
                    if val > 0:
                        for i in range(0, int(val * 10)):
                            tombola.append(Coordinate2D(x, z))
        return tombola

    def generate_coordinate(self):
        tombola = self.assemble_tombola()
        return random.choice(tombola)


class SparseHeatmap(Heatmap):
    def __init__(self, points: Dict["Coordinate2D", float]):
        super().__init__(HeatmapType.SPARSE.value, sparse=points)


class InverseSparseHeatmap(Heatmap):
    def __init__(self, values: Dict[float, List["Coordinate2D"]]):
        super().__init__(HeatmapType.INVERSE_SPARSE.value, inverse_sparse=values)


class MatrixHeatmap(Heatmap):
    def __init__(self, matrix: List[List[float]]):
        super().__init__(HeatmapType.MATRIX.value, matrix=matrix)
