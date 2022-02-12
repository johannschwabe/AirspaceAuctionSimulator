import random

from Simulator import Tick, Agent, PointOfInterest
from Simulator.Coordinate import Coordinate, TimeCoordinate


class AgentA(Agent):
    def __init__(self, dimensions: Coordinate, now: int):
        steps = random.randint(1, 5)
        desired_path = [PointOfInterest(Coordinate(random.randint(0, dimensions.x - 1),
                                                   random.randint(0, dimensions.y - 1),
                                                   random.randint(0, dimensions.z - 1)),
                                        Tick(now + random.randint(0, 10)))]
        for _ in range(steps):
            poi = TimeCoordinate(random.randint(0, dimensions.x - 1), random.randint(0, dimensions.y - 1),
                                 random.randint(0, dimensions.z - 1), Tick(0))
            distance = desired_path[-1].location.distance(poi, False)
            poi.t = desired_path[-1].tick + distance + random.randint(0, 5)
            desired_path.append(PointOfInterest(poi.to_inter_temporal(), poi.t))

        super().__init__(100, desired_path)
