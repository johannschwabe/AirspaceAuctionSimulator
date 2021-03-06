import random
from typing import List, TYPE_CHECKING

from ..Coordinate import TimeCoordinate
from .Owner import Owner
from ..Time import Tick
from ..Agent import ABCAgent

if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Agent import Agent


class ABCOwner(Owner):
    def __init__(self, name: str, color: str, creation_ticks: List[int]):
        super().__init__(name, color)
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            speed = 1
            start = self.valid_random_coordinate(env, Tick(t + random.randint(0, 10)), ABCAgent.default_near_radius,
                                                 speed)

            locations = [start]
            prev_location = start
            stays = []
            for i in range(random.randint(2, 5)):
                location = self.valid_random_coordinate(env, Tick(0), ABCAgent.default_near_radius,
                                                        speed)
                distance = prev_location.inter_temporal_distance(location)
                stay = random.randint(1, 3)
                stays.append(stay)
                t = prev_location.t + stay + (distance * speed) + random.randint(0, 5)
                location.t = t
                locations.append(location)
                prev_location = location

            agent = ABCAgent(locations, stays, speed=speed)
            res.append(agent)
            print(f"A-B-C created {agent}")

        self.agents += res
        return res
