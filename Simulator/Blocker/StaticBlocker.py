from rtree import Index

from .BlockerType import BlockerType
from .. import Blocker
from ..Coordinate import Coordinate4D, Coordinate3D


class StaticBlocker(Blocker):
    def __init__(self, location: Coordinate4D, dimension: Coordinate3D):
        super().__init__(dimension, blocker_type=BlockerType.STATIC)
        self.location = location

    def add_to_tree(self, tree: Index, dimension: Coordinate4D):
        max_pos = self.location + self.dimension
        max_pos.t = dimension.t
        tree_rep = self.location.list_rep() + max_pos.list_rep()
        tree.insert(self.id, tree_rep)
