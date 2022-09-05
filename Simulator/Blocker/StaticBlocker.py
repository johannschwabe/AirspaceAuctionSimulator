from typing import TYPE_CHECKING

from .Blocker import Blocker, EPSION
from .BlockerType import BlockerType
from ..Coordinates.Coordinate4D import Coordinate4D

if TYPE_CHECKING:
    from ..Coordinates.Coordinate3D import Coordinate3D
    from rtree import Index


class StaticBlocker(Blocker):
    blocker_type: str = BlockerType.STATIC.value

    def __init__(self, location: "Coordinate3D", dimension: "Coordinate3D"):
        super().__init__(dimension)
        self.location = location

    def add_to_tree(self, tree: "Index", dimension: "Coordinate4D"):
        assert self.id > -1
        max_pos_3d = self.location + self.dimension
        max_pos_4d = Coordinate4D.from_3d(max_pos_3d, dimension.t)
        max_pos_4d.x -= EPSION
        max_pos_4d.y -= EPSION
        max_pos_4d.z -= EPSION
        min_pos_4d = Coordinate4D.from_3d(self.location, 0)
        tree_rep = min_pos_4d.list_rep() + max_pos_4d.list_rep()
        tree.insert(self.id, tree_rep)
