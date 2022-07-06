import random
from typing import List

from BiddingAllocator.BiddingStationaryAgent import BiddingStationaryAgent
from Simulator import Environment
from Simulator.Agent import Agent
from Simulator.Coordinate import Coordinate4D
from Simulator.Owner.SpaceOwners.StationaryOwner import StationaryOwner


class BiddingStationaryOwner(StationaryOwner):
    def __init__(self,
                 name: str,
                 color: str,
                 creation_ticks: List[int],
                 nr_blocks: int,
                 size: "Coordinate4D",
                 priority: float):
        super().__init__(name, color, creation_ticks, nr_blocks, size)
        self.priority = priority

    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            dimensions = env._dimension
            blocks = []
            for i in range(self.nr_blocks):
                bottom_left = Coordinate4D.random(dimensions)
                top_right = bottom_left + self.size
                blocks.append([bottom_left, top_right])
            agent = BiddingStationaryAgent(blocks, self.priority)
            res.append(agent)
            print(f"Stationary created {agent}")

        self.agents += res
        return res
