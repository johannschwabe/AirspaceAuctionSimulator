from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

from ..Bid import Bid
from ..Coordinate import TimeCoordinate
from ..Path import PathSegment, SpaceSegment

if TYPE_CHECKING:
    from .. import Tick

class Agent(ABC):
    _id: int = 0

    def __init__(
        self,
    ):
        self.id = Agent._id
        Agent._id += 1
        self.is_clone = False

        self._allocated_segments: List[PathSegment|SpaceSegment] = []

        self.optimal_welfare: float = 1.
        self.costs: float = 0.

    @property
    def achieved_welfare(self) -> float:
        return self.value_for_segments(self._allocated_segments)

    @abstractmethod
    def value_for_segments(self, segments: List[PathSegment|SpaceSegment]) -> float:
        pass

    @abstractmethod
    def get_bid(self, t: "Tick") -> Bid:
        pass

    @abstractmethod
    def clone(self):
        pass

    def get_allocated_coords(self) -> List["TimeCoordinate"]:
        return [coord for path_segment in self._allocated_segments for coord in path_segment.coordinates]

    @abstractmethod
    def add_allocated_segment(self, segment: PathSegment|SpaceSegment):
        pass

    def get_allocated_segments(self) -> List["PathSegment|SpaceSegment"]:
        return self._allocated_segments

    def get_allocated_value(self) -> float:
        return self.value_for_segments(self._allocated_segments)

    def set_allocated_segments(self, segments: List["PathSegment|SpaceSegment"]):
        self._allocated_segments = segments

    def __repr__(self):
        return str(self.id)
