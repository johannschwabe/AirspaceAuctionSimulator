from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Coordinate import Coordinate4D, Coordinate3D

class PathSegment:
    def __init__(self, start: "Coordinate3D", end: "Coordinate3D", index: int, coords: List["Coordinate4D"]):
        self.coordinates = coords
        self.start = start
        self.end = end
        self.index = index

    def join(self, other: "PathSegment"):
        self.coordinates.extend(other.coordinates)

    def same(self, other: "PathSegment"):
        idx = self.index == other.index
        start_same = self.end == other.end
        if idx and not start_same:
            print("You done gufed")
        return idx and start_same

    def __str__(self):
        return f"{self.start} -> {self.end}: {self.index}"

    def clone(self):
        return PathSegment(self.start.clone(), self.end.clone(), self.index, [x.clone() for x in self.coordinates])

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
