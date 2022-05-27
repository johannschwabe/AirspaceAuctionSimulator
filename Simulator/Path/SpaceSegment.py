from typing import List

from .Segment import Segment
from ..Coordinate import TimeCoordinate


class SpaceSegment(Segment):
    def __init__(self, coords: List["TimeCoordinate"]):
        super().__init__(coords)
