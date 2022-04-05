from typing import List, Dict

from ..Coordinate import TimeCoordinate, Coordinate


class Blocker:
    def __init__(self, locations: List[TimeCoordinate], blocked_coordinates: List[Coordinate]):
        self._locations: Dict[int, TimeCoordinate] = {}
        for location in locations:
            self._locations[location.t] = location
        self.dimension: List[Coordinate] = blocked_coordinates
        self.origin = locations[0]

    def get_coordinates_at(self, t: int) -> List[Coordinate]:
        res = []
        for blocked in self.dimension:
            res.append(self._locations[t] + blocked)
        return res

    def is_blocked(self, coordinates: TimeCoordinate) -> bool:
        transformed_location = \
            coordinates.to_inter_temporal() - self._locations[min(int(coordinates.t), list(self._locations.keys())[-1])]
        return transformed_location in self.dimension
