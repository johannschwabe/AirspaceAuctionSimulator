from typing import List, Dict

from simulator.coordinates import TimeCoordinate, Coordinate


class Blocker:
    def __init__(self, locations: List[TimeCoordinate], blocked_coordinates: List[Coordinate]):
        self.locations: Dict[int, TimeCoordinate] = {}
        for location in locations:
            self.locations[location.t] = location
        self.blocked_coordinates: List[Coordinate] = blocked_coordinates

    def get_coordinates_at(self, t: int) -> List[Coordinate]:
        res = []
        for blocked in self.blocked_coordinates:
            res.append(self.locations[t] + blocked)
        return res

    def is_blocked(self, coordinates: TimeCoordinate) -> bool:
        transformed_location = coordinates.to_inter_temporal() - self.locations[coordinates.t]
        return transformed_location in self.blocked_coordinates

    def will_be_blocked(self, coordinates: TimeCoordinate, t: int) -> float:
        if self.is_blocked(coordinates):
            return 1.0
        return 0.0
