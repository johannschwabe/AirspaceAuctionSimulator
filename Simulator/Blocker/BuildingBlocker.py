from typing import List

from .StaticBlocker import StaticBlocker
from shapely.geometry import Polygon, Point, box
from ..Coordinate import Coordinate4D, Coordinate3D


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

    def is_box_blocking(self, bottom_left: "Coordinate4D", top_right: "Coordinate4D") -> bool:
        return self.polygon.intersects(box(bottom_left.x, bottom_left.z, top_right.x, top_right.z))
