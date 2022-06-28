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
            speed = 1
            start = self.valid_random_coordinate(env,
                                                 Tick(t),
                                                 BiddingABAgent.default_near_radius,
                                                 speed)
            target = self.valid_random_coordinate(env,
                                                  Tick(0),
                                                  BiddingABAgent.default_near_radius,
                                                  speed)
            distance = start.inter_temporal_distance(target)
            travel_time = distance * speed
            target.t = start.t + travel_time + random.randint(0, 5)
            agent = BiddingABAgent(start, target, self.priority, speed=speed, battery=travel_time * 2)
            res.append(agent)
            # print(f"A-B created {agent}")

        self.agents += res
        return res
