import random
from typing import List

from Simulator import Tick, Agent, PointOfInterest, Allocator
from Simulator.Coordinate import Coordinate, TimeCoordinate
from Simulator.Field import EnrichedField
from Simulator.Value import IndifferentValueFunction


class JohannAgent(Agent):
    def __init__(self, dimensions: Coordinate, now: int):
        steps = random.randint(1, 5)
        desired_path = [PointOfInterest(Coordinate(random.randint(0, dimensions.x - 1),
                                                   random.randint(0, dimensions.y - 1),
                                                   random.randint(0, dimensions.z - 1)),
                                        Tick(now + random.randint(0, 10)))]
        for _ in range(steps):
            poi = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                 random.randint(0, dimensions.y - 1),
                                 random.randint(0, dimensions.z - 1),
                                 Tick(0))
            distance = desired_path[-1].location.distance(poi)
            poi.t = desired_path[-1].tick + distance + random.randint(0, 5)
            desired_path.append(PointOfInterest(poi.to_inter_temporal(), poi.t))

        super().__init__(100, desired_path)

    def calculate_desired_path(self, allocator: Allocator, costs: List[EnrichedField]) -> List[PointOfInterest]:
        desired_path = self.points_of_interest.copy()
        start = self.points_of_interest[0].to_time_coordinate()
        for poi in self.points_of_interest[1:]:
            target = poi.to_time_coordinate()
            in_between_coords = allocator.get_shortest_path(start, target)[1:-1]
            in_between_pois = map(lambda tc: PointOfInterest(tc, tc.t), in_between_coords)
            for poi in in_between_pois:
                poi.set_spatial_value_function(IndifferentValueFunction())
            desired_path.extend(map())

        return list(map(lambda tc: PointOfInterest(tc, tc.t), desired_path))