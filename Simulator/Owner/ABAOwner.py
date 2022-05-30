import random
from typing import List, TYPE_CHECKING

from ..Agent import ABAAgent
from ..Coordinate import TimeCoordinate
from .Owner import Owner
from ..Time import Tick

if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Agent import Agent


class ABAOwner(Owner):
    def __init__(self, name: str, color: str, creation_ticks: List[int]):
        super().__init__(name, color)
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            dimensions = env._dimension
            speed = random.randint(1, 3)
            start = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                   0,
                                   random.randint(0, dimensions.z - 1),
                                   Tick(t + random.randint(0, 10)))
            while True:
                if env.is_blocked(start, ABAAgent.default_near_radius, speed):
                    break
                if start.y >= env.get_dim().y:
                    start = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                           0,
                                           random.randint(0, dimensions.z - 1),
                                           Tick(t + random.randint(0, 10)))
                start.y += 1
            target = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                    0,
                                    random.randint(0, dimensions.z - 1),
                                    Tick(0))
            while True:
                if env.is_blocked(target, ABAAgent.default_near_radius, speed):
                    break
                if target.y >= env.get_dim().y:
                    target = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                           0,
                                           random.randint(0, dimensions.z - 1),
                                           Tick(t + random.randint(0, 10)))
                target.y += 1
            stay = random.randint(1, 5)
            distance = start.inter_temporal_distance(target)
            target.t = start.t + stay + distance * speed + random.randint(0, 10)
            agent = ABAAgent(start, target, speed=speed, stay=stay, near_radius=0.3)
            res.append(agent)
            print(f"A-B-A created {agent}")

        self.agents += res
        return res
