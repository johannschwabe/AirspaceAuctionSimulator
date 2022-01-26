from typing import Optional

from simulator.allocators.Allocator import Allocator
from simulator.coordinates.Coordinates import Coordinates
from simulator.travel_path.TravelPath import TravelPath


class Agent:
    def __init__(self,
                 uuid: str,
                 revenue: float,
                 opportunity_cost: float,
                 risk_aversion: float):
        self.uuid = uuid
        self.revenue: float = revenue
        self.opportunity_cost: float = opportunity_cost
        self.risk_aversion: float = risk_aversion

        self.traveled_path: TravelPath = TravelPath([])
        self.optimal_path: Optional[TravelPath] = None
        self.allocated_path: Optional[TravelPath] = None

    def get_welfare(self, t1: int, t2: int) -> float:
        pass

    def get_location(self, t: int) -> Coordinates:
        pass

    def calculate_optimal_path(self, allocator: Allocator) -> TravelPath:
        pass

    def value_of_path(self, path: TravelPath) -> float:
        pass

    def buy_path(self, path: TravelPath):
        pass
