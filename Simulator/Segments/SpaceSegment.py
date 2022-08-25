from typing import TYPE_CHECKING, List, Tuple

from .Segment import Segment

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D


class SpaceSegment(Segment):
    def __init__(self, min_coordinates: "Coordinate4D", max_coordinates: "Coordinate4D"):
        self.min: "Coordinate4D" = min_coordinates
        self.max: "Coordinate4D" = max_coordinates

    def tree_rep(self) -> List[int]:
        return self.min.list_rep() + self.max.list_rep()

    def split_temporal(self, t: int) -> Tuple["SpaceSegment", "SpaceSegment"]:
        first_segment = self.clone()
        first_segment.max.t = t

        second_segment = self.clone()
        second_segment.min.t = t + 1

        return first_segment, second_segment

    def clone(self) -> "SpaceSegment":
        return SpaceSegment(self.min.clone(), self.max.clone())
