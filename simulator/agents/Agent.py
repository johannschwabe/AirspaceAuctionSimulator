from typing import Optional
import sys
from simulator.allocators.Allocator import Allocator
from typing import List
from simulator.coordinates.Coordinates import Coordinates
from simulator.travel_path.TravelPath import TravelPath


class Agent:
    def __init__(self,
                 uuid: str,
                 revenue: float,
                 opportunity_cost: float,
                 risk_aversion: float,
                 desired_path: TravelPath,
                 ):
        self.uuid = uuid
        self.revenue: float = revenue
        self.opportunity_cost: float = opportunity_cost
        self.risk_aversion: float = risk_aversion

        self.traveled_path: TravelPath = TravelPath([])
        self.desired_path: TravelPath = desired_path
        self.allocated_path: Optional[TravelPath] = None

    def get_welfare(self, t1: int, t2: int) -> float:
        pass

    def get_location(self, t: int) -> Coordinates:
        pass

    def calculate_desired_path(self) -> List[TravelPath]:
        return [self.desired_path]

    def cost_of_deviation(self):
        pass

    def value_of_path(self, path: TravelPath) -> float:
        min_path_cost = sys.float_info.max
        min_path = None
        for desired_path in self.calculate_desired_path():
            path_cost = 0.0
            for desired_location in desired_path.locations:
                min_cost = sys.float_info.max
                for path_location in path.locations:
                    spacial_error, temporal_error = desired_location.distance(path_location, True)
                    cost = Agent.cost_of_temporal_deviation(temporal_error) + Agent.cost_of_spacial_deviation(spacial_error)
                    min_cost = min(min_cost, cost)

                path_cost += min_cost
            if path_cost < min_path_cost:
                min_path_cost = path_cost
                min_path = desired_path

        return min_path_cost

    @staticmethod
    def cost_of_spacial_deviation(distance: float):
        return distance**2

    @staticmethod
    def cost_of_temporal_deviation(distance: float):
        return distance**3


    def buy_path(self, path: TravelPath):
        pass

    def __repr__(self):
        return str(self.uuid)