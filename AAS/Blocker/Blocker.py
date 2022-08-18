from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Coordinates.Coordinate3D import Coordinate3D
    from rtree import Index


class Blocker(ABC):
    blocker_type: str

    def __init__(self, dimension: "Coordinate3D"):
        self.dimension: Coordinate3D = dimension
        self.id: int = -1

    def is_blocking(self, _coord: "Coordinate4D", _radius: int = 0):
        return True

    def is_box_blocking(self, _bottom_left: "Coordinate4D", _top_right: "Coordinate4D") -> bool:
        return True

    @abstractmethod
    def add_to_tree(self, tree: "Index", dimension: "Coordinate4D", blocker_id: int):
        pass
