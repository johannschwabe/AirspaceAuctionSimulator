from typing import List, Dict

from simulator.coordinates.Coordinates import Coordinates
from simulator.coordinates.TimeCoordinates import TimeCoordinates


class Blocker:
    def __init__(self, locations: List[TimeCoordinates], blocked_coordinates: List[Coordinates]):
        self.locations: Dict[int, TimeCoordinates] = {}
        for location in locations:
            self.locations[location.t] = location
        self.blocked_coordinates: List[Coordinates] = blocked_coordinates

    def get_coordinates_at(self, t: int) -> List[Coordinates]:
        res = []
        for blocked in self.blocked_coordinates:
            res.append(self.locations[t] + blocked)
        return res

    def is_blocked(self, coordinates: TimeCoordinates) -> bool:
        transformed_location = coordinates.to_inter_temporal() - self.locations[coordinates.t]
        return transformed_location in self.blocked_coordinates

    def will_be_blocked(self, coordinates: TimeCoordinates, t: int) -> float:
        if self.is_blocked(coordinates):
            return 1.0
        return 0.0
