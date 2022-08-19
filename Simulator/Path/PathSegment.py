from typing import List, TYPE_CHECKING, Tuple

from .Segment import Segment

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Coordinates.Coordinate3D import Coordinate3D


class PathSegment(Segment):
    def __init__(self, start: "Coordinate3D", end: "Coordinate3D", index: int, coordinates: List["Coordinate4D"]):
        self.coordinates: List["Coordinate4D"] = coordinates
        self.start: "Coordinate3D" = start
        self.end: "Coordinate3D" = end
        self.index: int = index

    def join(self, other: "PathSegment"):
        self.coordinates.extend(other.coordinates)

    def same(self, other: "PathSegment"):
        same_index = self.index == other.index
        same_end = self.end == other.end
        if same_index and not same_end:
            print(f"Same index ({self.index} == {other.index}) but not same end ({self.end} != {other.end})")
        return same_index and same_end

    @property
    def min(self):
        return self.coordinates[0]

    @property
    def max(self):
        return self.coordinates[-1]

    def clone(self):
        return PathSegment(self.start.clone(), self.end.clone(), self.index, [x.clone() for x in self.coordinates])

    def split_temporal(self, t: int) -> Tuple["PathSegment", "PathSegment"]:
        t_index = t - self.coordinates[0].t
        first_segment = self.clone()
        first_segment.coordinates = first_segment.coordinates[:t_index + 1]

        second_segment = self.clone()
        second_segment.coordinates = second_segment.coordinates[t_index + 1:]

        return first_segment, second_segment
