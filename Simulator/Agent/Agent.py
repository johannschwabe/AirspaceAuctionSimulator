from abc import ABC
from typing import Optional, List, Dict

from ..Allocator import Allocator
from ..Field import EnrichedField
from ..PointOfInterest import PointOfInterest
from ..Path import TravelPath
from ..Value import RangeValueFunction, IndifferentValueFunction


class Agent(ABC):
    id = 0

    def __init__(self,
                 revenue: float,
                 points_of_interest: List[PointOfInterest],
                 uuid: str = None):
        self.allocator: Optional[Allocator] = None
        if uuid is None:
            self.uuid: str = str(Agent.id)
            Agent.id += 1
        self.revenue: float = revenue

        self.traveled_path: TravelPath = TravelPath([])
        self.points_of_interest: List[PointOfInterest] = points_of_interest
        self.allocated_path: Optional[TravelPath] = None

        self.value_of_flight_time = RangeValueFunction(0, 30)  # After 30 ticks, drone is dead and the value is always 0

    def register(self, allocator: Allocator):
        self.allocator = allocator

    def calculate_desired_path(self, costs: Dict[str, float] = None) -> List[PointOfInterest]:
        return self.points_of_interest

    def connect_pois(self, poi_1, poi_2):
        assert self.allocator is not None
        start = poi_1.to_time_coordinate()
        target = poi_2.to_time_coordinate()
        in_between_coords = self.allocator.get_shortest_path(start, target)[1:-1]
        in_between_pois = map(lambda tc: PointOfInterest(tc, tc.t), in_between_coords)
        for ib_poi in in_between_pois:
            ib_poi.set_spatial_value_function(IndifferentValueFunction())
            ib_poi.set_temporal_value_function(IndifferentValueFunction())
        return in_between_pois

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
        new_agent.uuid = f"clone({self.uuid})"
        return new_agent

    def __repr__(self):
        return f"{self.uuid}: {self.points_of_interest}"

    def __str__(self):
        return f"{self.uuid}: {self.points_of_interest}"
