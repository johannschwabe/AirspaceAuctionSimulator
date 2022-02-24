from typing import List

from ..Coordinate import TimeCoordinate

class Agent:

    def __init__(self, locations: List[TimeCoordinate], welfare: float, costs: float):
        self.locations: List[TimeCoordinate] = locations
        self.welfare: float = welfare
        self.costs: float = costs
        self.flight_time = locations[-1].t - locations[0].t

