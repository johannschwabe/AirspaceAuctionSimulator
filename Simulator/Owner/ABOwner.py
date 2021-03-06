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
            speed = 1
            start = self.valid_random_coordinate(env,
                                                 Tick(t + random.randint(0, 10)),
                                                 ABAgent.default_near_radius,
                                                 speed)
            target = self.valid_random_coordinate(env, Tick(0),  ABAgent.default_near_radius, speed)

            distance = start.inter_temporal_distance(target)
            travel_time = distance * speed
            target.t = start.t + travel_time + random.randint(0, 5)
            agent = ABAgent(start, target, speed=speed, battery=travel_time * 2)
            res.append(agent)
            print(f"A-B created {agent}")

        self.agents += res
        return res
