from typing import List

from simulator.coordinates.Coordinates import Coordinates
from simulator.coordinates.TimeCoordinates import TimeCoordinates


class Blocker:
    def __init__(self, locations: List[TimeCoordinates], blocked_coordinates: List[Coordinates]):
        self.locations: List[TimeCoordinates] = locations
        self.blocked_coordinates: List[Coordinates] = blocked_coordinates

    def get_coordinates_at(self, t: int) -> List[Coordinates]:
        pass

    def is_blocked(self, coordinates: TimeCoordinates) -> bool:
        pass

    def will_be_blocked(self, coordinates: TimeCoordinates) -> float:
        pass
