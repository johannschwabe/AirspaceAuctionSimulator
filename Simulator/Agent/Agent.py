from abc import ABC, abstractmethod,ABCMeta
from typing import List, TYPE_CHECKING

from ..Bid import Bid
from ..Coordinate import Coordinate4D

if TYPE_CHECKING:
    from ..Path import PathSegment, SpaceSegment


class Agent(ABC):
    _id: int = 0

    def __init__(
        self,
        agent_type: str,
        allocation_type: str,
    ):
        self.id = Agent._id
        Agent._id += 1
        self.is_clone = False

        self.agent_type = agent_type
        self.allocation_type = allocation_type

        self._allocated_segments: List["PathSegment | SpaceSegment"] = []

        self.optimal_welfare: float = 1.
        self.costs: float = 0.

    @property
    def achieved_welfare(self) -> float:
        return self.value_for_segments(self._allocated_segments)

    @abstractmethod
    def value_for_segments(self, segments: List["PathSegment | SpaceSegment"]) -> float:
        pass

    @abstractmethod
    def get_bid(self, t: int) -> Bid:
        pass

    @abstractmethod
    def clone(self):
        pass

    def get_allocated_coords(self) -> List["Coordinate4D"]:
        return [coord for path_segment in self._allocated_segments for coord in path_segment.coordinates]

    @abstractmethod
    def add_allocated_segment(self, segment: "PathSegment | SpaceSegment"):
        pass

    def get_allocated_segments(self) -> List["PathSegment|SpaceSegment"]:
        return self._allocated_segments

    def get_allocated_value(self) -> float:
        return self.value_for_segments(self._allocated_segments)

    def set_allocated_segments(self, segments: List["PathSegment|SpaceSegment"]):
        self._allocated_segments = segments

    def generalized_bid(self):
        return {
            "No Bid": "-",
            "!value": -1
        }

    def __repr__(self):
        return str(self.id)
