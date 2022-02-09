from typing import List

from simulator.Coordinates.TimeCoordinates import TimeCoordinate


class TravelPath:

    def __init__(self, locations: List[TimeCoordinate]):
        self.locations: List[TimeCoordinate] = locations
