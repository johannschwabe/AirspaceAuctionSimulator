from typing import List

from Simulator import Agent, PointOfInterest, Allocator
from Simulator.Coordinate import TimeCoordinate
from Simulator.Field import EnrichedField


class AToBAgent(Agent):
    def __init__(self, a: TimeCoordinate, b: TimeCoordinate, value: float = 100):
        points_of_interest = [PointOfInterest(a, a.t), PointOfInterest(b, b.t)]
        super().__init__(value, points_of_interest)

    def calculate_desired_path(self, allocator: Allocator, costs: List[EnrichedField]) -> List[PointOfInterest]:
        start = self.points_of_interest[0].to_time_coordinate()
        target = self.points_of_interest[1].to_time_coordinate()
        desired_path = allocator.get_shortest_path(start, target)
        return list(map(lambda tc: PointOfInterest(tc, tc.t), desired_path))
