import random
from typing import List

from Simulator import Environment, Owner, Tick
from Simulator.Agent import Agent, StationaryAgent
from Simulator.Coordinate import Coordinate


class StationaryOwner(Owner):
    def __init__(self, creation_ticks: List[int]):
        super().__init__()
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: Environment) -> List[Agent]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            dimensions = env._dimension
            corner_1 = Coordinate(
                random.randint(0, dimensions.x // 2),
                random.randint(0, dimensions.y // 2),
                random.randint(0, dimensions.z // 2),
            )
            corner_2 = Coordinate(
                random.randint(corner_1.x, dimensions.x - 1),
                random.randint(corner_1.y, dimensions.y - 1),
                random.randint(corner_1.z, dimensions.z - 1),
            )

            block = []

            for x in range(corner_1.x, corner_2.x + 1):
                for y in range(corner_1.y, corner_2.y + 1):
                    for z in range(corner_1.z, corner_2.z + 1):
                        block.append(Coordinate(x, y, z))

            t_start = t + random.randint(0, 10)
            t_end = t_start + random.randint(5, 10)

            agent = StationaryAgent(block, Tick(t_start), Tick(t_end))
            res.append(agent)
            print(f"Stationary created {agent}")

        self.agents += res
        return res
