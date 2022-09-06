from typing import List, TYPE_CHECKING

from shapely.geometry import Polygon, Point, box

from .StaticBlocker import StaticBlocker

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Coordinates.Coordinate3D import Coordinate3D


class BuildingBlocker(StaticBlocker):
    def __init__(self, vertices: List[List[float]], bounds: List["Coordinate3D"], holes: List[List[List[float]]]):
        super().__init__(bounds[0], bounds[1] - bounds[0])
        self.points = vertices
        self.holes = holes
        self.polygon = Polygon(vertices, holes)
        
    def is_blocking(self, coord: "Coordinate4D", radius: int = 0):
        point = Point(coord.x, coord.z)
        if radius == 0:
            return self.polygon.intersects(point)
        near_bound = point.buffer(radius)
        return self.polygon.intersects(near_bound)

    def is_box_blocking(self, bottom_left: "Coordinate4D", top_right: "Coordinate4D") -> bool:
        return self.polygon.intersects(box(bottom_left.x, bottom_left.z, top_right.x, top_right.z))
