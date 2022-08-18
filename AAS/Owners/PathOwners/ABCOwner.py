import random
from typing import TYPE_CHECKING

from AAS.Owners.PathOwner import PathOwner

if TYPE_CHECKING:
    from ...Agents.ABCAgent import ABCAgent
    from ..GridLocation import GridLocation
    from ...Simulator import Simulator


class ABCOwner(PathOwner):
    label = "A to B to C"
    description = "A owner with agents going from A to a number of stops"
    min_locations = 2
    max_locations = 100
    meta = []

    def __init__(self, name: str, color: str, stops: list["GridLocation"], creation_ticks: list[int]):
        assert len(stops) > 1

        super().__init__(name, color, stops)
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, simulator: "Simulator") -> list["ABCAgent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            speed = 1
            start = self.generate_stop_coordinate(self.stops[0], simulator.environment, t, 1, speed)

            stays = []
            locations = [start]
            for stop in self.stops[1:]:
                next_location = self.generate_stop_coordinate(stop, simulator.environment, t, 1, speed)

                stay = random.randint(0, 100)
                stays.append(stay)
                distance = locations[-1].inter_temporal_distance(next_location)
                travel_time = distance * speed
                next_location.t = min(locations[-1].t + travel_time + stay + random.randint(0, 100),
                                      simulator.environment.get_dim().t)
                locations.append(next_location)

            agent = ABCAgent(locations, stays, simulator, speed=speed)
            res.append(agent)
            print(f"A-B-C created {agent}, {','.join([str(loc) for loc in locations])}")

        self.agents += res
        return res
