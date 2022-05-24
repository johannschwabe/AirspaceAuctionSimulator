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
            dimensions = env._dimension
            start = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                   random.randint(0, 0),
                                   random.randint(0, dimensions.z - 1),
                                   Tick(t + random.randint(0, 10)))
            locations = [start]
            prev_location = start
            speed = random.randint(1, 3)
            stays = []
            for i in range(3):
                location = TimeCoordinate(
                    random.randint(0, dimensions.x - 1),
                    random.randint(0, 0),
                    random.randint(0, dimensions.z - 1),
                    Tick(0)
                )

                distance = prev_location.inter_temporal_distance(location)
                stay = random.randint(1, 3)
                stays.append(stay)
                t = prev_location.t + stay + (distance * speed) + random.randint(0, 5)
                location.t = t
                locations.append(location)
                prev_location = location

            agent = ABCAgent(locations, stays[:-1], speed=speed)
            res.append(agent)
            print(f"A-B-C created {agent}")

        self.agents += res
        return res
