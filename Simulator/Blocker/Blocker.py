from abc import ABC, abstractmethod

from rtree import Index

from .BlockerType import BlockerType
from ..Coordinate import Coordinate4D, Coordinate3D


class Blocker(ABC):
    _id: int = 1

    blocker_type: str

    def __init__(self, dimension: Coordinate3D):
        self.id = -Blocker._id
        Blocker._id += 1
        self.dimension: Coordinate3D = dimension

    def is_blocking(self, coord: Coordinate4D, radius: int = 0):
        return True

    def is_box_blocking(self, bottom_left: Coordinate4D, top_right: Coordinate4D) -> bool:
        return True

    @abstractmethod
    def add_to_tree(self, tree: Index, dimension: Coordinate4D):
        pass
