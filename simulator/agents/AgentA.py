import random

from simulator.agents.Agent import Agent
from simulator.coordinates.Coordinates import Coordinates
from simulator.coordinates.TimeCoordinates import TimeCoordinates


class AgentA(Agent):
    def __init__(self, dimensions: Coordinates, now: int):
        steps = random.randint(1, 5)
        desired_path = [TimeCoordinates(random.randint(0, dimensions.x), random.randint(0, dimensions.y),
                                        random.randint(0, dimensions.z), now + random.randint(0, 10))]
        for _ in range(steps):
            poi = TimeCoordinates(random.randint(0, dimensions.x), random.randint(0, dimensions.y), random.randint(0, dimensions.z), 0)
            distance, _ = desired_path[-1].distance(poi, False)
            poi.t = distance + random.randint(0,5)
            desired_path.append(poi)

        super().__init__(100, 0, 0, desired_path)
