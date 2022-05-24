from typing import List, Dict

from ..Coordinate import TimeCoordinate, Coordinate


class Blocker:
    _id: int = 1

    def __init__(self, locations: List[TimeCoordinate], dimension: Coordinate):
        self.id = -Blocker._id
        Blocker._id += 1
        self.locations = locations
        self.dimension: Coordinate = dimension

    def add_to_tree(self, tree):
        if not self.locations or len(self.locations) == 0:
            return
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

    def get_coordinates_at(self, t: int) -> List[Coordinate]:
        t -= self.locations[0]
        res = []
        for x in range(self.dimension.x):
            for y in range(self.dimension.y):
                for z in range(self.dimension.z):
                    res.append(Coordinate(self.locations[t].x + x, self.locations[t].y + y, self.locations[t].z + z))
        return res
