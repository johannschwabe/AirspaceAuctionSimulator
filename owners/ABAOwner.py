import random
from typing import List

from Simulator import Environment, Owner, Tick
from Simulator.Agent import Agent, ABAAgent
from Simulator.Coordinate import TimeCoordinate


class ABAOwner(Owner):
    def __init__(self, creation_ticks: List[int]):
        super().__init__()
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: Environment) -> List[Agent]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            dimensions = env.dimension
            start = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                   random.randint(0, dimensions.y - 1),
                                   random.randint(0, dimensions.z - 1),
                                   Tick(t + random.randint(0, 10)))
            target = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                    random.randint(0, dimensions.y - 1),
                                    random.randint(0, dimensions.z - 1),
                                    Tick(0))
            speed = random.randint(1, 3)
            distance = start.inter_temporal_distance(target)
            target.t = start.t + distance * speed + random.randint(0, 10)
            agent = ABAAgent(start, target, speed=speed, stay=random.randint(1, 5))
            res.append(agent)
            print(f"A-B-A created {agent}")

        self.agents += res
        return res
