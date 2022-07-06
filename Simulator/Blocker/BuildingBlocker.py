from typing import List

from shapely.geometry import Polygon, Point
from .StaticBlocker import StaticBlocker
from ..Coordinate import Coordinate4D


class BuildingBlocker(StaticBlocker):
    def __init__(self, vertices: List[List[int]], bounds: List[Coordinate4D]):
        super().__init__(bounds[0], bounds[1] - bounds[0])

        self.points = vertices
        self.polygon = Polygon(vertices)

    def is_blocking(self, coord: Coordinate4D, radius: int = 0):
        point = Point(coord.x, coord.z)

        if radius == 0:
            return self.polygon.intersects(point)
        near_bound = point.buffer(radius)
        return self.polygon.intersects(near_bound)
