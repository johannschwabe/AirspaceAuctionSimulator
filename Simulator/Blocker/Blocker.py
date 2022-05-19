from typing import List, Dict

from ..Coordinate import TimeCoordinate, Coordinate


class Blocker:
    _id: int = 0

    def __init__(self, locations: List[TimeCoordinate], dimension: Coordinate):
        self.id = -Blocker._id
        Blocker._id += 1
        self.locations = locations
        self.dimension: Coordinate = dimension

    def add_to_tree(self, tree):
        if not self.locations or len(self.locations) == 0:
            return
        iter = 0
        while iter < len(self.locations):
            start = self.locations[iter]
            while self.locations[iter].inter_temporal_equal(start) and iter < len(self.locations):
                iter += 1
            min_pos = start + self.dimension
            tree_rep = min_pos.tree_query_rep()
            tree_rep[7] = self.locations[iter].t - 1
            tree.insert(self.id, tree_rep)

    def get_coordinates_at(self, t: int) -> List[Coordinate]:
        t -= self.locations[0]
        res = []
        for x in range(self.dimension.x):
            for y in range(self.dimension.y):
                for z in range(self.dimension.z):
                    res.append(Coordinate(self.locations[t].x + x, self.locations[t].y + y, self.locations[t].z + z))
        return res
