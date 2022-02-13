from typing import List

from Simulator import Agent, PointOfInterest, Tick, Allocator
from Simulator.Coordinate import Coordinate
from Simulator.Field import EnrichedField


class HobbyPilotAgent(Agent):
    def __init__(self, corner1: Coordinate, corner2: Coordinate, t_start: int, t_stop: int, value: float = 100):
        assert corner1 <= corner2
        assert t_start <= t_stop

        points_of_interest = []
        for t in range(t_start, t_stop + 1):
            for x in range(corner1.x, corner2.x + 1):
                for y in range(corner1.y, corner2.y + 1):
                    for z in range(corner1.z, corner2.z + 1):
                        points_of_interest.append(PointOfInterest(Coordinate(x, y, z), Tick(t)))

        super().__init__(value, points_of_interest)

    def calculate_desired_path(self, allocator: Allocator, costs: List[EnrichedField]) -> List[PointOfInterest]:
        desired_path = self.points_of_interest
        for t in map(lambda ef: ef.coordinate.t, costs):
            desired_path = filter(lambda poi: poi.tick != t, desired_path)

        return desired_path
