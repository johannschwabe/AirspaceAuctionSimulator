from typing import List

from ..Agent import Agent
from ..Coordinate import TimeCoordinate
from ..IO import Stringify


class Field(Stringify):
    def __init__(self, coordinates: TimeCoordinate):
        self.coordinates: TimeCoordinate = coordinates

        self._allocated_to: List[Agent] = []
        self._near_to: List[Agent] = []
        self._far_to: List[Agent] = []

    def is_allocated(self) -> bool:
        return len(self._allocated_to) > 0

    def is_near(self) -> bool:
        return len(self._near_to) > 0

    def is_far(self) -> bool:
        return len(self._far_to) > 0

    def __repr__(self):
        if self._allocated_to is None:
            return f"{self.coordinates.__repr__()}, empty"
        return f"{self.coordinates.__repr__()}, {self._allocated_to.__repr__()}"
