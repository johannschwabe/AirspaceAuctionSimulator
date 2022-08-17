import random
from typing import List, TYPE_CHECKING

from AAS.Owner import GridLocation
from AAS.Owner.PathOwner import PathOwner
from AAS.Agent import ABAgent

if TYPE_CHECKING:
    from AAS import Environment
    from AAS.Agent import Agent


class ABOwner(PathOwner):
    label = "A to B"
    description = "Owner with agents going from A to B"
    min_locations = 2
    max_locations = 2
    meta = []

    def __init__(self, name: str, color: str, stops: List[GridLocation], creation_ticks: List[int]):
        assert len(stops) == 2

        super().__init__(name, color, stops)
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: "Environment") -> List["Agents"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            speed = 1
            start = self.generate_stop_coordinate(self.stops[0], env, t, 1, speed)
            target = self.generate_stop_coordinate(self.stops[-1], env, t, 1, speed)

            distance = start.inter_temporal_distance(target)
            travel_time = distance * speed
            target.t = min(start.t + travel_time + random.randint(0, 100), env.get_dim().t)
            agent = ABAgent(start, target, speed=speed, battery=travel_time * 2)
            res.append(agent)
            print(f"A-B created {str(agent)}: {start} -> {target}")

        self.agents += res
        return res
