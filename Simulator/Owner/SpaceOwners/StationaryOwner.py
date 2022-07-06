import random
from typing import List, TYPE_CHECKING

from Simulator.Coordinate import Coordinate3D, Coordinate4D
from Simulator.Owner.SpaceOwner import SpaceOwner
from Simulator.Agent import StationaryAgent

if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Agent import Agent


class StationaryOwner(SpaceOwner):
    def __init__(self, name: str, color: str, creation_ticks: List[int], nr_blocks: int, size: Coordinate4D):
        super().__init__(name, color)
        self.creation_ticks = creation_ticks
        self.nr_blocks: int = nr_blocks
        self.size: "Coordinate4D" = size

    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            dimensions = env._dimension
            blocks = []
            for i in range(self.nr_blocks):
                bottom_left = Coordinate4D.random(dimensions)
                top_right = bottom_left + self.size
                blocks.append([bottom_left, top_right])
            agent = StationaryAgent(blocks)
            res.append(agent)
            print(f"Stationary created {agent}")

        self.agents += res
        return res
