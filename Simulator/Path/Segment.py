from typing import List
from ..Coordinate import TimeCoordinate

class Segment:
    def __init__(self, coordinates: List["TimeCoordinate"]):
        self.coordinates = coordinates
