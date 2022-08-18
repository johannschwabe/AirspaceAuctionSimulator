import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ..PathOwner import PathOwner

if TYPE_CHECKING:
    from ...Coordinates.Coordinate4D import Coordinate4D
    from ...Agents.ABAAgent import ABAAgent
    from ..GridLocation import GridLocation
    from ...Simulator import Simulator


class ABAOwner(PathOwner, ABC):
    min_locations = 2
    max_locations = 2
    meta = []

    def __init__(self, name: str, color: str, stops: List["GridLocation"], creation_ticks: List[int]):
        assert len(stops) == 2

        super().__init__(name, color, stops)
        self.creation_ticks = creation_ticks

    @abstractmethod
    def initialize_agent(self,
                         start: "Coordinate4D",
                         target: "Coordinate4D",
                         simulator: "Simulator",
                         speed: int,
                         battery: int,
                         stay: int) -> "ABAAgent":
        pass

    def generate_agents(self, t: int, simulator: "Simulator") -> List["ABAAgents"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            speed = 1
            start = self.generate_stop_coordinate(self.stops[0], simulator.environment, t, 1, speed)
            target = self.generate_stop_coordinate(self.stops[-1], simulator.environment, t, 1, speed)

            stay = random.randint(0, 100)
            distance = start.inter_temporal_distance(target)
            travel_time = distance * speed
            target.t = min(start.t + travel_time + stay + random.randint(0, 100), simulator.environment.get_dim().t)
            battery = travel_time * 4
            agent = self.initialize_agent(start, target, simulator, speed, battery, stay)
            res.append(agent)
            print(f"A-B-A created {agent}: {start} --> {target}")

        self.agents += res
        return res
