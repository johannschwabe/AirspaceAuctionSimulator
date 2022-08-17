import random
from typing import List, TYPE_CHECKING

from Demos.Bidding.Agents.BiddingABAgent import BiddingABAgent
from AAS.Owner import GridLocation
from AAS.Owner.PathOwners.ABOwner import ABOwner

if TYPE_CHECKING:
    from AAS import Environment


class BiddingABOwner(ABOwner):
    label = "Bidding A to B"
    description = "A bidding owner with a priority going from A to B"
    meta = []

    def __init__(self, name: str, color: str, stops: List[GridLocation], creation_ticks: List[int],
                 priority: float = None):
        super().__init__(name, color, stops, creation_ticks)
        self.priority = priority if priority else random.random() * 10

    def generate_agents(self, t: int, env: "Environment") -> List["Agents"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            speed = 1
            start = self.generate_stop_coordinate(self.stops[0], env, t, 1, speed)
            target = self.generate_stop_coordinate(self.stops[-1], env, t, 1, speed)

            distance = start.inter_temporal_distance(target)
            travel_time = distance * speed
            target.t = min(start.t + travel_time + random.randint(0, 100), env.get_dim().t)
            agent = BiddingABAgent(start, target, priority=random.randint(0, 100), speed=speed, battery=travel_time * 2)
            res.append(agent)
            print(f"A-B created {agent}")

        self.agents += res
        return res
