from typing import List, Tuple

from .Segment import Segment
from ..Coordinates.Coordinate4D import Coordinate4D


class SpaceSegment(Segment):
    def __init__(self, min_coordinates: "Coordinate4D", max_coordinates: "Coordinate4D", index: int):
        super().__init__(index)
        self._min: "Coordinate4D" = min_coordinates
        self._max: "Coordinate4D" = max_coordinates

    def tree_rep(self) -> List[float]:
        return self.min.list_rep() + self.max.list_rep()

    def split_temporal(self, t: int) -> Tuple["SpaceSegment", "SpaceSegment"]:
        first_segment = self.clone()
        first_segment.max.t = t

        second_segment = self.clone()
        second_segment.min.t = t + 1

        return first_segment, second_segment

    @property
    def nr_voxels(self) -> float:
        return abs(self.min.x - self.max.x) * abs(self.min.y - self.max.y) * abs(self.min.z - self.max.z) * abs(
            self.min.t - self.max.t)

    @property
    def min(self) -> "Coordinate4D":
        return self._min

    @property
    def max(self) -> "Coordinate4D":
        return self._max

    @property
    def dimension(self) -> "Coordinate4D":
        return self.max - self.min

    def contains(self, coordinate: "Coordinate4D") -> bool:
        return self.min <= coordinate < self.max

    def intersecting_space(self, other: "SpaceSegment") -> "Tuple[Coordinate4D,Coordinate4D]":
        if not (self.min < other.max and other.min < self.max):
            return Coordinate4D(0, 0, 0, 0), Coordinate4D(0, 0, 0, 0)
        min_x = self.min.x if self.min.x > other.min.x else other.min.x
        max_x = self.max.x if self.max.x < other.max.x else other.max.x
        min_y = self.min.y if self.min.y > other.min.y else other.min.y
        max_y = self.max.y if self.max.y < other.max.y else other.max.y
        min_z = self.min.z if self.min.z > other.min.z else other.min.z
        max_z = self.max.z if self.max.z < other.max.z else other.max.z
        min_t = self.min.t if self.min.t > other.min.t else other.min.t
        max_t = self.max.t if self.max.t < other.max.t else other.max.t
        return Coordinate4D(min_x, min_y, min_z, min_t), Coordinate4D(max_x, max_y, max_z, max_t),

    def intersection_volume(self, other: "SpaceSegment"):
        _min, _max = self.intersecting_space(other)
        if _max - _min > Coordinate4D(0, 0, 0, 0):
            return _max - _min
        return Coordinate4D(0, 0, 0, 0)

    def clone(self) -> "SpaceSegment":
        return SpaceSegment(self.min.clone(), self.max.clone(), self.index)

    def __str__(self):
        return f"SpaceSegment: {self.min} -> {self.max}"
