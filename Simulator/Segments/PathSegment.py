from typing import List, TYPE_CHECKING, Tuple

from .Segment import Segment

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Coordinates.Coordinate3D import Coordinate3D


class PathSegment(Segment):
    def __init__(self, start: "Coordinate3D", end: "Coordinate3D", index: int, coordinates: List["Coordinate4D"]):
        super().__init__(index)
        self._coordinates: List["Coordinate4D"] = coordinates
        self.validate()
        self.start: "Coordinate3D" = start
        self.end: "Coordinate3D" = end

    def validate(self):
        _iter = self._coordinates[0]
        for coord in self._coordinates[1:]:
            if not coord.t == _iter.t + 1 or coord.distance(_iter) > 1:
                print(f"{coord} - {_iter}")
            assert coord.distance(_iter) <= 1
            assert coord.t == _iter.t + 1
            _iter = coord

    def join(self, other: "PathSegment"):
        join_index = 0
        if other.min == self.max:
            join_index = 1
        elif other.min.inter_temporal_equal(self.max):
            join_index = self.max.t - other.min.t + 1
        else:
            print(f"other: {other.min.t}, self: {self.max.t}")
            assert other.min.t == self.max.t + 1

        self.coordinates.extend(other.coordinates[join_index:])
        self.validate()

    def same(self, other: "PathSegment"):
        same_index = self.index == other.index
        if same_index:
            assert self.end == other.end
        return same_index

    @property
    def coordinates(self) -> List["Coordinate4D"]:
        return self._coordinates

    @property
    def nr_voxels(self) -> int:
        return len(self.coordinates)

    @property
    def min(self) -> "Coordinate4D":
        return self.coordinates[0]

    @property
    def max(self) -> "Coordinate4D":
        return self.coordinates[-1]

    def clone(self):
        return PathSegment(self.start.clone(), self.end.clone(), self.index, [x.clone() for x in self.coordinates])

    def contains(self, coordinate: "Coordinate4D") -> bool:
        return coordinate in self.coordinates

    def split_temporal(self, t: int) -> Tuple["PathSegment", "PathSegment"]:
        t_index = t - self.min.t
        first_segment = self.clone()
        first_segment._coordinates = first_segment.coordinates[:t_index + 1]

        second_segment = self.clone()
        second_segment._coordinates = second_segment.coordinates[t_index + 1:]

        return first_segment, second_segment

    def __str__(self):
        return f"PathSegment: {self.min} -> {self.max}"
