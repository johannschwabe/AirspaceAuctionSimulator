from typing import List, TYPE_CHECKING

from ..Coordinate import TimeCoordinate
from ..IO import Stringify

if TYPE_CHECKING:
    from ..Agent import Agent

class Field(Stringify):
    def __init__(self, coordinates: TimeCoordinate):
        self.coordinates: TimeCoordinate = coordinates

        self._allocated_to: List["Agent"] = []
        self._near_to: List["Agent"] = []
        self._far_to: List["Agent"] = []

    def get_allocated(self):
        return self._allocated_to

    def add_allocation(self, new_agent: "Agent"):
        if new_agent not in self._allocated_to:
            self._allocated_to.append(new_agent)

    def remove_allocation_of_agent(self, to_remove: "Agent"):
        self._allocated_to.remove(to_remove)

    def get_near(self):
        return self._near_to

    def add_near(self, new_agent: "Agent"):
        if new_agent not in self._near_to:
            self._near_to.append(new_agent)

    def remove_near_to_of_agent(self, to_remove: "Agent"):
        self._near_to.remove(to_remove)

    def get_far(self):
        return self._far_to

    def add_far(self, new_agent: "Agent"):
        if new_agent not in self._far_to:
            self._far_to.append(new_agent)

    def remove_far_to_of_agent(self, to_remove: "Agent"):
        self._far_to.remove(to_remove)

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
