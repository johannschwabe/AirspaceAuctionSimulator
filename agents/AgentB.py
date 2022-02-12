import random

from Simulator import Tick, Agent, PointOfInterest
from Simulator.Coordinate import Coordinate, TimeCoordinate


class AgentB(Agent):
    def __init__(self, dimensions: Coordinate, now: int):
        desired_path = [PointOfInterest(Coordinate(random.randint(0, dimensions.x - 1),
                                                   random.randint(0, dimensions.y - 1),
                                                   random.randint(0, dimensions.z - 1)),
                                        Tick(now + random.randint(0, 10)))]

        target = TimeCoordinate(random.randint(0, dimensions.x - 1), random.randint(0, dimensions.y - 1),
                                random.randint(0, dimensions.z - 1), Tick(0))
        distance = desired_path[-1].location.distance(target, False)
        target.t = desired_path[-1].tick + distance + random.randint(0, 5)
        desired_path.append(PointOfInterest(target.to_inter_temporal(), target.t))

        super().__init__(100, desired_path)
