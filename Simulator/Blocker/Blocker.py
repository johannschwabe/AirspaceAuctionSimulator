from typing import List, Dict

from ..Coordinate import TimeCoordinate, Coordinate


class Blocker:
    def __init__(self, locations: List[TimeCoordinate], dimension: Coordinate):
        self.locations: Dict[int, TimeCoordinate] = {}
        for location in locations:
            self.locations[location.t] = location
        self.dimension: Coordinate = dimension

    def get_coordinates_at(self, t: int) -> List[Coordinate]:
        res = []
        for x in range(self.dimension.x):
            for y in range(self.dimension.y):
                for z in range(self.dimension.z):
                    res.append(Coordinate(self.locations[t].x + x, self.locations[t].y + y, self.locations[t].z + z))
        return res

    def is_blocked(self, coordinate: TimeCoordinate) -> bool:
        blocked = self.get_coordinates_at(coordinate.t)
        return coordinate.to_inter_temporal() in blocked
