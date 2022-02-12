import random
from typing import List

from Simulator import Agent, Environment, Owner, Tick
from Simulator.Coordinate import TimeCoordinate
from agents.AToBAgent import AToBAgent


class OwnerB(Owner):
    def __init__(self, creation_ticks: List[int]):
        super().__init__()
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: Environment) -> List[Agent]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            print(f"creating agent #{Agent.id}")
            dimensions = env.dimension
            start = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                   random.randint(0, dimensions.y - 1),
                                   random.randint(0, dimensions.z - 1),
                                   Tick(t + random.randint(0, 10)))
            target = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                    random.randint(0, dimensions.y - 1),
                                    random.randint(0, dimensions.z - 1),
                                    Tick(0))
            distance = start.inter_temporal_distance(target)
            target.t = start.t + distance + random.randint(0, 5)
            res.append(AToBAgent(start, target))

        self.agents += res
        return res
