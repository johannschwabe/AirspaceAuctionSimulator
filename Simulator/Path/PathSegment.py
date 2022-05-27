from typing import List, TYPE_CHECKING

from .Segment import Segment
from ..Coordinate import Coordinate
if TYPE_CHECKING:
    from ..Coordinate import TimeCoordinate

class PathSegment(Segment):
    def __init__(self, start: Coordinate, end: Coordinate, index: int, path: List["TimeCoordinate"]):
        super().__init__(path)
        self.start = start
        self.end = end
        self.index = index

    def join(self, other: "PathSegment"):
        self.coordinates.extend(other.coordinates)

    def same(self, other: "PathSegment"):
        idx = self.index == other.index
        start_end = self.start == other.start and self.end == other.end
        if idx and not start_end:
            print("You done gufed")
        return idx and start_end

    def __str__(self):
        return f"{self.start} -> {self.end}: {self.index}"

    def clone(self):
        return PathSegment(self.start.clone(), self.end.clone(), self.index, [x.clone() for x in self.coordinates])

