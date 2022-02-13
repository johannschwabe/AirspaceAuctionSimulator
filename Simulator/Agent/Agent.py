import random
from abc import ABC
from typing import Optional, List

from ..Allocator import Allocator
from ..Field import EnrichedField
from ..PointOfInterest import PointOfInterest
from ..Path import TravelPath
from ..Value import RangeValueFunction


class Agent(ABC):
    id = 0

    def __init__(self,
                 revenue: float,
                 points_of_interest: List[PointOfInterest],
                 ):
        self.uuid = Agent.id
        Agent.id += 1
        self.revenue: float = revenue

        self.traveled_path: TravelPath = TravelPath([])
        self.points_of_interest: List[PointOfInterest] = points_of_interest
        self.allocated_path: Optional[TravelPath] = None

        self.value_of_flight_time = RangeValueFunction(0, 30)  # After 30 ticks, drone is dead and the value is always 0

    def calculate_desired_path(self, allocator: Allocator, costs: List[EnrichedField]) -> List[PointOfInterest]:
        return self.points_of_interest

    def value_of_path(self, path: TravelPath) -> float:
        path_value = 1
        for pos in self.points_of_interest:
            path_value *= pos.value_of_path(path)

        flight_time = path[-1].t - path[0].t
        flight_time_value = self.value_of_flight_time(flight_time)

        return path_value * self.revenue * flight_time_value

    def clone(self):
        new_agent = Agent(self.revenue,
                          [poi.clone() for poi in self.points_of_interest])
        new_agent.uuid = self.uuid + 10000 * random.randint(1, 1000)
        return new_agent

    def __repr__(self):
        return f"{self.uuid}: {self.points_of_interest}"

    def __str__(self):
        return f"{self.uuid}: {self.points_of_interest}"
