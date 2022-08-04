import random
from typing import List, TYPE_CHECKING

from BiddingAllocator.BiddingStationaryAgent import BiddingStationaryAgent
from Simulator import Environment
from Simulator.Agent import Agent
from Simulator.Coordinate import Coordinate4D
from Simulator.Owner.SpaceOwners.StationaryOwner import StationaryOwner

if TYPE_CHECKING:
    from Simulator.Owner import PathStop


class BiddingStationaryOwner(StationaryOwner):
    label = "Bidding Stationary"
    description = "A bidding owner interested in a set of cubes"

    def __init__(self,
                 name: str,
                 color: str,
                 stops: List["PathStop"],
                 creation_ticks: List[int],
                 size: "Coordinate4D" = Coordinate4D(5, 5, 5, 5),
                 priority: float = None):
        super().__init__(name, color, stops, creation_ticks, size)
        self.priority = priority if priority else random.random() * 10

    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            blocks = []
            for stop in self.stops:
                bottom_left = self.generate_stop_coordinates(stop, env, t, self.size)
                top_right = bottom_left + self.size
                blocks.append([bottom_left, top_right])
            agent = BiddingStationaryAgent(blocks, self.priority)
            res.append(agent)
            print(f"Bidding Stationary created {agent}")

        self.agents += res
        return res
