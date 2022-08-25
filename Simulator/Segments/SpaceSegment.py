from typing import TYPE_CHECKING, List, Tuple

from .Segment import Segment

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D


class SpaceSegment(Segment):
    def __init__(self, min_coordinates: "Coordinate4D", max_coordinates: "Coordinate4D"):
        self._min: "Coordinate4D" = min_coordinates
        self._max: "Coordinate4D" = max_coordinates

    def tree_rep(self) -> List[int]:
        return self.min.list_rep() + self.max.list_rep()

    def split_temporal(self, t: int) -> Tuple["SpaceSegment", "SpaceSegment"]:
        first_segment = self.clone()
        first_segment.max.t = t

        second_segment = self.clone()
        second_segment.min.t = t + 1

        return first_segment, second_segment

    @property
    def nr_voxels(self) -> int:
        return abs(self.min.x - self.max.x) * abs(self.min.y - self.max.y) * abs(self.min.z - self.max.z) * abs(
            self.min.t - self.max.t)

    @property
    def min(self) -> "Coordinate4D":
        return self._min

    @property
    def max(self) -> "Coordinate4D":
        return self._max

    def clone(self) -> "SpaceSegment":
        return SpaceSegment(self.min.clone(), self.max.clone())
