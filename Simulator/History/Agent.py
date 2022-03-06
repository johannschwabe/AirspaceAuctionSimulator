from typing import List
import uuid

from ..Coordinate import TimeCoordinate

class Agent:

    def __init__(self, locations: List[TimeCoordinate], optimal_welfare: float, achieved_welfare: float, costs: float):
        self.uuid = str(uuid.uuid4())
        self.locations: List[TimeCoordinate] = locations
        self.optimal_welfare: float = optimal_welfare
        self.achieved_welfare: float = achieved_welfare
        self.costs: float = costs
        self.flight_time = locations[-1].t - locations[0].t

    def clone(self):
        new_agent = Agent(self.locations.copy(), self.optimal_welfare, self.achieved_welfare, self.costs)
        new_agent.uuid = self.uuid #Probably a bad Idea
        return new_agent

    def __repr__(self):
        return self.uuid

