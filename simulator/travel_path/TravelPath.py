from typing import List

from simulator.coordinates.TimeCoordinates import TimeCoordinates


class TravelPath:

    def __init__(self, locations: List[TimeCoordinates]):
        self.locations: List[TimeCoordinates] = locations
