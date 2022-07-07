from rtree import Index

from .BlockerType import BlockerType
from .. import Blocker
from ..Coordinate import Coordinate4D, Coordinate3D


class StaticBlocker(Blocker):
    blocker_type: str = BlockerType.STATIC.value

    def __init__(self, location: Coordinate3D, dimension: Coordinate3D):
        super().__init__(dimension)
        self.location = location

    def add_to_tree(self, tree: Index, dimension: Coordinate4D):
        max_pos_3D = self.location + self.dimension
        max_pos_4D = Coordinate4D.from_3d(max_pos_3D, dimension.t)
        min_pos_4D = Coordinate4D.from_3d(self.location, 0)
        tree_rep = min_pos_4D.list_rep() + max_pos_4D.list_rep()
        tree.insert(self.id, tree_rep)
