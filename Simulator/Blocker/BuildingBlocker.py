from typing import List

from shapely.geometry import Polygon, Point, box
from . import Blocker
from ..Coordinate import Coordinate4D, Coordinate3D


class BuildingBlocker(Blocker):
    def __init__(self, vertices: List[List[float]], bounds: List[Coordinate4D], holes: List[List[float]]):
        self.points = vertices
        self.polygon = Polygon(vertices, holes)

        super().__init__(bounds, bounds[1] - bounds[0])

    def is_blocking(self, coord: Coordinate4D, radius: int = 0):
        point = Point(coord.x, coord.z)

        if radius == 0:
            return self.polygon.intersects(point)
        near_bound = point.buffer(radius)
        return self.polygon.intersects(near_bound)

    def is_box_blocking(self, bottom_left: "Coordinate4D", top_right: "Coordinate4D") -> bool:
        return self.polygon.intersects(box(bottom_left.x, bottom_left.z, top_right.x, top_right.z))

    def add_to_tree(self, tree):
        bbox = self.locations[0].list_rep() + self.locations[1].list_rep()
        bbox[1] = -1
        tree.insert(self.id, bbox)
