import random
from typing import List, TYPE_CHECKING

from Simulator.Agent import ABAAgent
from Simulator.Coordinate import TimeCoordinate
from Simulator.Owner.PathOwner import PathOwner
from Simulator.Time import Tick

if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Agent import Agent


class ABAOwner(PathOwner):
    def __init__(self, name: str, color: str, creation_ticks: List[int]):
        super().__init__(name, color)
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            speed = random.randint(1, 3)
            start = self.valid_random_coordinate(env,
                                                 Tick(t + random.randint(0, 10)),
                                                 ABAAgent.default_near_radius,
                                                 speed)

            target = self.valid_random_coordinate(env, Tick(0),  ABAAgent.default_near_radius, speed)

            stay = random.randint(1, 5)
            distance = start.inter_temporal_distance(target)
            target.t = start.t + stay + distance * speed + random.randint(0, 10)
            agent = ABAAgent(start, target, speed=speed, stay=stay, near_radius=0.3)
            res.append(agent)
            print(f"A-B-A created {agent}")

        self.agents += res
        return res
