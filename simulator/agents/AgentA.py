import random

from simulator.agents.Agent import Agent
from simulator.coordinates.Coordinates import Coordinates
from simulator.coordinates.TimeCoordinates import TimeCoordinates
from simulator.travel_path.TravelPath import TravelPath


class AgentA(Agent):
    def __init__(self, dimensions: Coordinates, now: int):
        steps = random.randint(1, 5)
        desired_path = [TimeCoordinates(random.randint(0, dimensions.x - 1), random.randint(0, dimensions.y - 1),
                                        random.randint(0, dimensions.z - 1), now + random.randint(0, 10))]
        for _ in range(steps):
            poi = TimeCoordinates(random.randint(0, dimensions.x - 1), random.randint(0, dimensions.y - 1), random.randint(0, dimensions.z - 1), 0)
            distance, _ = desired_path[-1].distance(poi, False)
            poi.t = desired_path[-1].t + distance + random.randint(0,5)
            desired_path.append(poi)

        super().__init__(100, 0, 0, TravelPath(desired_path))
