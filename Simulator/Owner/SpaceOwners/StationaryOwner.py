import random
from typing import List, TYPE_CHECKING

from Simulator.Coordinate import Coordinate3D
from Simulator.Owner.SpaceOwner import SpaceOwner
from Simulator.Agent import StationaryAgent

if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Agent import Agent


class StationaryOwner(SpaceOwner):
    def __init__(self, name: str, color: str, creation_ticks: List[int]):
        super().__init__(name, color)
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            dimensions = env.dimension
            corner_1 = Coordinate3D(
                random.randint(0, dimensions.x - 1),
                0,
                random.randint(0, dimensions.z - 1),
            )
            corner_2 = Coordinate3D(
                min(corner_1.x + random.randint(1, 10), dimensions.x - 1),
                min(corner_1.y + random.randint(1, 10), dimensions.y - 1),
                min(corner_1.z + random.randint(1, 10), dimensions.z - 1),
            )

            block = []

            for x in range(corner_1.x, corner_2.x + 1):
                for y in range(corner_1.y, corner_2.y + 1):
                    for z in range(corner_1.z, corner_2.z + 1):
                        block.append(Coordinate3D(x, y, z))

            t_start = t + random.randint(0, 10)
            t_end = t_start + random.randint(5, 10)

            agent = StationaryAgent(block, t_start, t_end)
            res.append(agent)
            print(f"Stationary created {agent}")

        self.agents += res
        return res
