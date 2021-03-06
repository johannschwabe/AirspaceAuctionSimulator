from typing import List

from shapely.geometry import Polygon, Point
from . import Blocker
from .. import Tick
from ..Coordinate import TimeCoordinate, Coordinate


class BuildingBlocker(Blocker):
    def __init__(self, vertices: List[List[int]], bounds: List[TimeCoordinate]):
        self.points = vertices
        self.polygon = Polygon(vertices)

        super().__init__(bounds, bounds[1]-bounds[0])


    def is_blocking(self, coord: TimeCoordinate, radius: int = 0):
        point = Point(coord.x, coord.z)

        if radius == 0:
            return self.polygon.intersects(point)
        near_bound = point.buffer(radius)
        return self.polygon.intersects(near_bound)

    def add_to_tree(self, tree):
        bbox = self.locations[0].list_rep() + self.locations[1].list_rep()
        bbox[1] = -1
        tree.insert(self.id, bbox)

