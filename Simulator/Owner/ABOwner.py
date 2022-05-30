import random
from typing import List, TYPE_CHECKING

from ..Coordinate import TimeCoordinate
from .Owner import Owner
from ..Time import Tick
from ..Agent import ABAgent

if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Agent import Agent


class ABOwner(Owner):
    def __init__(self, name: str, color: str, creation_ticks: List[int]):
        super().__init__(name, color)
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            dimensions = env._dimension
            # speed = random.randint(1, 3)
            speed = 1
            start = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                   0,
                                   random.randint(0, dimensions.z - 1),
                                   Tick(t + random.randint(0, 10)))
            while True:
                if not env.is_blocked(start, ABAgent.default_near_radius, speed):
                    break
                start.y += 1
                if start.y >= env.get_dim().y:
                    start = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                           0,
                                           random.randint(0, dimensions.z - 1),
                                           Tick(t + random.randint(0, 10)))

            target = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                    0,
                                    random.randint(0, dimensions.z - 1),
                                    Tick(0))
            while True:
                if not env.is_blocked(target, ABAgent.default_near_radius, speed):
                    break
                target.y += 1
                if target.y >= env.get_dim().y:
                    target = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                           0,
                                           random.randint(0, dimensions.z - 1),
                                           Tick(t + random.randint(0, 10)))
            distance = start.inter_temporal_distance(target)
            travel_time = distance * speed
            target.t = start.t + travel_time + random.randint(0, 5)
            agent = ABAgent(start, target, speed=speed, battery=travel_time * 2)
            res.append(agent)
            print(f"A-B created {agent}")

        self.agents += res
        return res
