from abc import ABC, abstractmethod
from typing import Tuple, TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D


class Segment(ABC):
    @abstractmethod
    def clone(self):
        pass

    @property
    @abstractmethod
    def coordinates(self) -> List["Coordinate4D"]:
        pass

    @abstractmethod
    def split_temporal(self, t: int) -> Tuple["Segment", "Segment"]:
        pass

    @property
    @abstractmethod
    def nr_voxels(self) -> int:
        pass

    @property
    @abstractmethod
    def min(self) -> "Coordinate4D":
        pass

    @property
    @abstractmethod
    def max(self) -> "Coordinate4D":
        pass
