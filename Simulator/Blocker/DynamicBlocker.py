from typing import List, TYPE_CHECKING

from .Blocker import Blocker
from .BlockerType import BlockerType

if TYPE_CHECKING:
    from Simulator.Coordinates.Coordinate4D import Coordinate4D
    from Simulator.Coordinates.Coordinate3D import Coordinate3D
    from rtree import Index


class DynamicBlocker(Blocker):
    blocker_type: str = BlockerType.DYNAMIC.value

    def __init__(self, locations: List["Coordinate4D"], dimension: "Coordinate3D"):
        super().__init__(dimension)
        self.locations = locations

    def add_to_tree(self, tree: "Index", dimension: "Coordinate4D"):
        assert self.id > -1
        idx = 0
        start = self.locations[idx]
        while idx < len(self.locations):
            end = None
            if not self.locations[idx].inter_temporal_equal(start):
                end = self.locations[idx - 1]
            elif idx == len(self.locations) - 1:
                end = self.locations[idx]
            if end is not None:
                max_pos = start + self.dimension
                max_pos.t = end.t
                tree_rep = start.list_rep() + max_pos.list_rep()
                tree.insert(self.id, tree_rep)
                start = self.locations[idx]
            idx += 1
