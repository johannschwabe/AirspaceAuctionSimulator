from abc import ABC, abstractmethod
from typing import Optional, List, Dict, TYPE_CHECKING

from ..PointOfInterest import PointOfInterest
from ..Path import TravelPath
from ..Value import RangeValueFunction, IndifferentValueFunction

if TYPE_CHECKING:
    from ..Allocator import Allocator


class Agent(ABC):
    id = 0

    def __init__(self,
                 revenue: float,
                 points_of_interest: List[PointOfInterest],
                 uuid: Optional[str] = None):
        self.revenue = revenue
        self.points_of_interest = points_of_interest
        if uuid is None:
            self.uuid: str = str(Agent.id)
            Agent.id += 1
        else:
            self.uuid: str = uuid

        self.not_today = False
        self.allocator: Optional["Allocator"] = None
        self.traveled_path: TravelPath = TravelPath([])
        self.allocated_path: Optional[TravelPath] = None
        self.value_of_flight_time = RangeValueFunction(0, 30)  # After 30 ticks, drone is dead and the value is always 0

    def register(self, allocator: "Allocator"):
        self.allocator = allocator

    def calculate_desired_path(self, costs: Dict[str, float] = None) -> List[PointOfInterest]:
        return self.points_of_interest

    def connect_pois(self, poi_1, poi_2):
        assert self.allocator is not None
        start = poi_1.to_time_coordinate()
        target = poi_2.to_time_coordinate()
        in_between_coords = self.allocator.get_shortest_path(start, target)
        if in_between_coords is None:
            return None
        in_between_coords = in_between_coords[1:-1]
        in_between_pois = list(map(lambda tc: PointOfInterest(tc, tc.t), in_between_coords))
        for ib_poi in in_between_pois:
            ib_poi.set_spatial_value_function(IndifferentValueFunction())
            ib_poi.set_temporal_value_function(IndifferentValueFunction())
        return in_between_pois

    def value_of_path(self, path: TravelPath) -> float:
        if len(path) == 0:
            return 0
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
        return f"{self.uuid}"

    def __str__(self):
        return f"{self.uuid}"
