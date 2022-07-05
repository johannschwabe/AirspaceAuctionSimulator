import random
from typing import List, TYPE_CHECKING

from Simulator.Agent import ABAAgent
from Simulator.Owner import PathStop
from Simulator.Owner.PathOwner import PathOwner

if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Agent import Agent


class ABAOwner(PathOwner):
    def __init__(self, name: str, color: str, stops: List[PathStop], creation_ticks: List[int]):
        assert len(stops) == 2

        super().__init__(name, color, stops)
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            speed = 1
            start = self.generate_stop_coordinate(self.stops[0], env, t + random.randint(0, 100), 1, speed)
            target = self.generate_stop_coordinate(self.stops[-1], env, t, 1, speed)

            stay = random.randint(0, 100)
            distance = start.inter_temporal_distance(target)
            travel_time = distance * speed
            target.t = start.t + travel_time + stay + random.randint(0, 100)
            agent = ABAAgent(start, target, speed=speed, battery=travel_time * 4, stay=stay)
            res.append(agent)
            print(f"A-B-A created {agent}: {start} --> {target}")

        self.agents += res
        return res
