from typing import List
from random import random, choice

from .Owner import Owner
from .Agent import Agent
from .History import History

from ..Coordinate import TimeCoordinate, SaveTimeCoordinate


class Generator:

    def __init__(self, name: str, description: str, agents: int, owners: int, dimensions: TimeCoordinate, avg_flight_time: int):
        self.name: str = name
        self.description: str = description
        self.n_agents: int = agents
        self.n_owners: int = owners
        self.dimensions: TimeCoordinate = dimensions
        self.avg_flight_time: int = avg_flight_time
        self.owners: List[Owner] = []

    def simulate(self):
        self.simulate_ticks()


    def simulate_ticks(self):
        for owner in range(self.n_owners):
            self.owners.append(Owner())

        for i in range(self.n_agents):
            random_start_location = TimeCoordinate.random(self.dimensions)
            locations = [SaveTimeCoordinate.from_time_coordinate(random_start_location, dimensions=self.dimensions)]
            chance_x = random()
            chance_y = (1 - chance_x) * random()
            chance_forward = random() ** 2
            chance_forward *= -1 if random() > 0.5 else 1
            while random() > 1 / self.avg_flight_time and locations[-1].t < (self.dimensions.t - 1):
                loc = locations[-1]
                next_loc = loc.random_neighbor(1, chance_x=chance_x, chance_y=chance_y, chance_forward=chance_forward)
                locations.append(next_loc)
            welfare = random() * 10
            costs = random() * 5
            agent = Agent(locations, welfare, costs)
            choice(self.owners).add_agent(agent)

    @property
    def history(self):
        return History(self.name, self.description, self.dimensions, self.owners)
