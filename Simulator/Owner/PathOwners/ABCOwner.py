import random
from typing import List, TYPE_CHECKING

from Simulator.Owner import PathStop
from Simulator.Owner.PathOwner import PathOwner
from Simulator.Agent import ABCAgent

if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Agent import Agent


class ABCOwner(PathOwner):
    def __init__(self, name: str, color: str, stops: List[PathStop], creation_ticks: List[int]):
        assert len(stops) > 1

        super().__init__(name, color, stops)
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            speed = 1
            start = self.generate_stop_coordinate(self.stops[0], env, t + random.randint(0, 100), 1, speed)

            stays = []
            locations = [start]
            for stop in self.stops[1:]:
                next_location = self.generate_stop_coordinate(stop, env, t, 1, speed)

                stay = random.randint(0, 100)
                stays.append(stay)
                distance = locations[-1].inter_temporal_distance(next_location)
                travel_time = distance * speed
                next_location.t = locations[-1].t + travel_time + stay + random.randint(0, 100)
                locations.append(next_location)

            agent = ABCAgent(locations, stays, speed=speed)
            res.append(agent)
            print(f"A-B-C created {agent}")

        self.agents += res
        return res