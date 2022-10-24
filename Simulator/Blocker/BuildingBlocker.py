import math
from typing import List, TYPE_CHECKING

import shapely.errors
from shapely.geometry import Point, Polygon, box

from .StaticBlocker import StaticBlocker

if TYPE_CHECKING:
    from Simulator.Coordinates.Coordinate4D import Coordinate4D
    from Simulator.Coordinates.Coordinate3D import Coordinate3D


class BuildingBlocker(StaticBlocker):
    def __init__(self,
                 vertices: List[List[float]],
                 bounds: List["Coordinate3D"],
                 holes: List[List[List[float]]],
                 osm_id=None):
        """
        :param bounds: assert len(bounds) == 2
        """
        assert len(bounds) == 2
        super().__init__(bounds[0], bounds[1] - bounds[0])
        self.points = vertices
        self.holes = holes
        self.polygon = Polygon(vertices, holes)
        self.osm_id = osm_id

    def is_blocking(self, coord: "Coordinate4D", radius: int = 0):
        point = Point(coord.x, coord.z)
        if radius == 0:
            return self.polygon.intersects(point)
        max_height = self.location.y + self.dimension.y
        min_height = self.location.y
        if coord.y > max_height or coord.y < min_height:
            height_dif = max(coord.y - max_height, min_height - coord.y)
            corrected_radius = math.sqrt(
                math.pow(radius, 2) - math.pow(height_dif, 2))
        else:
            corrected_radius = radius
        near_bound = point.buffer(corrected_radius)
        return self.intersects(near_bound)

    def intersects(self, intersection):
        try:
            return self.polygon.intersects(intersection)
        except shapely.errors.TopologicalError:
            self.polygon = Polygon(self.points)
            return self.polygon.intersects(intersection)

    def is_box_blocking(self, bottom_left: "Coordinate4D", top_right: "Coordinate4D") -> bool:
        return self.intersects(box(bottom_left.x, bottom_left.z, top_right.x, top_right.z))
