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
        self.__i = 0

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

    def __getitem__(self, n):
        return self.coordinates[n]

    def __len__(self):
        return len(self.coordinates)

    def __iter__(self):
        self.__i = 0
        return self

    def __next__(self):
        if self.__i < len(self.coordinates):
            loc = self.coordinates[self.__i]
            self.__i += 1
            return loc
        raise StopIteration
