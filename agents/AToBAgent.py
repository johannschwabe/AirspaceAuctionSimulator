from typing import List, Dict

from Simulator import Agent, PointOfInterest
from Simulator.Coordinate import TimeCoordinate


class AToBAgent(Agent):
    def __init__(self, a: TimeCoordinate, b: TimeCoordinate, value: float = 100):
        points_of_interest = [PointOfInterest(a, a.t), PointOfInterest(b, b.t)]
        super().__init__(value, points_of_interest)

    def calculate_desired_path(self, costs: Dict[str, float] = None) -> List[PointOfInterest]:
        assert self.allocator is not None
        desired_path = self.points_of_interest.copy()
        start = self.points_of_interest[0]
        target = self.points_of_interest[1]
        in_between_pois = self.connect_pois(start, target)
        if in_between_pois is None:
            self.not_today = True
            return []
        desired_path.extend(in_between_pois)
        desired_path.sort(key=lambda x: x.tick)
        return desired_path
