import random
from typing import List

from Simulator import Environment, Owner
from Simulator.Time import Tick
from Simulator.Agent import ABAgent, Agent
from Simulator.Coordinate import TimeCoordinate


class ABOwner(Owner):
    def __init__(self, creation_ticks: List[int]):
        super().__init__()
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: Environment) -> List[Agent]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            dimensions = env._dimension
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
            travel_time = distance * speed
            target.t = start.t + travel_time + random.randint(0, 5)
            agent = ABAgent(start, target, speed=speed, battery=travel_time * 2)
            res.append(agent)
            # print(f"A-B created {agent}")

        self.agents += res
        return res
