import math
import random
from abc import abstractmethod
from typing import TYPE_CHECKING, List

from ..PathOwner import PathOwner

if TYPE_CHECKING:
    from ...Agents.PathAgents.ABCAgent import ABCAgent
    from ...Owners.Location.GridLocation import GridLocation
    from ...Simulator import Simulator
    from ...Coordinates.Coordinate4D import Coordinate4D


class ABCOwner(PathOwner):
    min_locations = 2
    max_locations = 100
    meta = []

    def __init__(self, owner_id: int, name: str, color: str, stops: List["GridLocation"], creation_ticks: List[int]):
        assert len(stops) > 1

        super().__init__(owner_id, name, color, stops)
        self.creation_ticks = creation_ticks

    @abstractmethod
    def initialize_agent(self,
                         locations: List["Coordinate4D"],
                         stays: List[int],
                         simulator: "Simulator",
                         speed: int,
                         battery: int,
                         near_radius: int) -> "ABCAgent":
        pass

    def generate_agents(self, t: int, simulator: "Simulator") -> List["ABCAgent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            speed = 1
            near_radius = 1
            start = self.generate_stop_coordinate(self.stops[0], simulator.environment, t, near_radius, speed)

            stays: List[int] = []
            locations: List["Coordinate4D"] = [start]
            total_travel_time: int = 0
            for stop in self.stops[1:]:
                next_location = self.generate_stop_coordinate(stop, simulator.environment, t, near_radius, speed)

                stay = random.randint(0, 100)
                stays.append(stay)
                distance = locations[-1].inter_temporal_distance(next_location)
                travel_time = math.ceil(distance) * speed
                total_travel_time += travel_time
                next_location.t = min(locations[-1].t + travel_time + stay + random.randint(0, 100),
                                      simulator.environment.dimension.t)
                locations.append(next_location)

            battery = total_travel_time * 4
            agent = self.initialize_agent(locations, stays, simulator, speed, battery, near_radius)
            res.append(agent)
            print(f"A-B-C created {agent}, {','.join([str(loc) for loc in locations])}")

        self.agents += res
        return res
