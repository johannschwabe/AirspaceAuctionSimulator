from typing import Optional, List

from ..Path import TravelPath
from ..PointOfInterest import PointOfInterest
from ..Value import RangeValueFunction
from ..coordinates import Coordinate


class Agent:
    id = 0

    def __init__(self,
                 revenue: float,
                 opportunity_cost: float,
                 risk_aversion: float,
                 points_of_interest: List[PointOfInterest],
                 ):
        self.uuid = Agent.id
        Agent.id += 1
        self.revenue: float = revenue
        self.opportunity_cost: float = opportunity_cost
        self.risk_aversion: float = risk_aversion

        self.traveled_path: TravelPath = TravelPath([])
        self.points_of_interest: List[PointOfInterest] = points_of_interest
        self.allocated_path: Optional[TravelPath] = None

        self.value_of_flight_time = RangeValueFunction(0, 30)  # After 30 ticks, drone is dead and the value is always 0

    def get_welfare(self, t1: int, t2: int) -> float:
        pass

    def get_location(self, t: int) -> Coordinate:
        pass

    def calculate_desired_path(self) -> List[PointOfInterest]:
        return self.points_of_interest

    def cost_of_deviation(self):
        pass

    def value_of_flight_time(self):
        return

    def value_of_path(self, path: TravelPath) -> float:
        path_value = 1
        for pos in self.points_of_interest:
            path_value *= pos.value_of_path(path)

        flight_time = path[-1].t - path[0].t
        flight_time_value = self.value_of_flight_time(flight_time)

        return path_value * self.revenue * flight_time_value

    def buy_path(self, path: TravelPath):
        pass

    def __repr__(self):
        return str(self.uuid)
