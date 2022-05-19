import random
from typing import List, TYPE_CHECKING

from BiddingAllocator.BiddingABAgent import BiddingABAgent
from Simulator.Coordinate import TimeCoordinate
from Simulator.Owner.ABOwner import ABOwner
from Simulator import Tick
if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Agent import Agent

class BiddingABOwner(ABOwner):
    def __init__(self, name: str, color: str, creation_ticks: List[int], priority: float):
        super().__init__(name, color, creation_ticks)
        self.priority = priority


    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            dimensions = env._dimension
            start = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                   random.randint(0, dimensions.y - 1),
                                   random.randint(0, dimensions.z - 1),
                                   Tick(t))
            target = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                    random.randint(0, dimensions.y - 1),
                                    random.randint(0, dimensions.z - 1),
                                    Tick(0))
            speed = random.randint(1, 3)
            distance = start.inter_temporal_distance(target)
            travel_time = distance * speed
            target.t = start.t + travel_time + random.randint(0, 5)
            agent = BiddingABAgent(start, target, self.priority, speed=speed, battery=travel_time * 2)
            res.append(agent)
            print(f"A-B created {agent}")

        self.agents += res
        return res
