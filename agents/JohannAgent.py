import random
from typing import List, Dict

from Simulator import Tick, Agent, PointOfInterest
from Simulator.Coordinate import Coordinate, TimeCoordinate


class JohannAgent(Agent):
    def __init__(self, dimensions: Coordinate, now: int):
        steps = random.randint(1, 5)
        desired_path = [PointOfInterest(Coordinate(random.randint(0, dimensions.x - 1),
                                                   random.randint(0, dimensions.y - 1),
                                                   random.randint(0, dimensions.z - 1)),
                                        Tick(now + random.randint(0, 10)))]
        for _ in range(steps):
            next_coord = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                        random.randint(0, dimensions.y - 1),
                                        random.randint(0, dimensions.z - 1),
                                        Tick(0))
            distance = desired_path[-1].location.inter_temporal_distance(next_coord)
            next_coord.t = desired_path[-1].tick + (distance + random.randint(0, 5))
            desired_path.append(PointOfInterest(next_coord, next_coord.t))

        super().__init__(100, desired_path)

    def calculate_desired_path(self, costs: Dict[str, float] = None) -> List[PointOfInterest]:
        assert self.allocator is not None
        desired_path = self.points_of_interest.copy()
        start = self.points_of_interest[0]
        for target in self.points_of_interest[1:]:
            in_between_pois = self.connect_pois(start, target)
            if in_between_pois is None:
                self.not_today = True
                return []
            desired_path.extend(in_between_pois)
            start = target

        desired_path.sort(key=lambda x: x.tick)
        return desired_path
