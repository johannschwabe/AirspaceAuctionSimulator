import math
import random
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from Simulator import PathAgent, PathOwner
from .WebOwnerMixin import WebOwnerMixin

if TYPE_CHECKING:
    from Simulator import BiddingStrategy, ValueFunction, Coordinate4D, Environment
    from ...GridLocation.GridLocation import GridLocation


class WebPathOwner(WebOwnerMixin, PathOwner):
    def __init__(self, owner_id: str,
                 name: str,
                 color: str,
                 stops: List["GridLocation"],
                 creation_ticks: List[int],
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction",
                 near_radius: float,
                 battery: int,
                 speed: int,
                 config: Optional[Dict[str, Any]] = None):
        super().__init__(name, color, creation_ticks, owner_id, bidding_strategy, value_function, config=config)
        assert near_radius >= 1
        self.stops = stops
        self.near_radius = near_radius
        self.battery = battery
        self.speed = speed

    def initialize_agent(self,
                         locations: List["Coordinate4D"],
                         stays: List[int]) -> "PathAgent":
        agent_id: str = self.get_agent_id()
        return PathAgent(agent_id, self.bidding_strategy, self.value_function, locations, stays,
                         speed=self.speed,
                         battery=self.battery,
                         near_radius=self.near_radius,
                         config=self.config)

    @staticmethod
    def generate_stop_coordinate(stop: "GridLocation", env: "Environment", t: int,
                                 near_radius: float) -> "Coordinate4D":
        coord = stop.generate_coordinates(env, t + 1)

        while coord.y < env.min_height or env.is_coordinate_blocked_forever(coord, near_radius):
            coord.y += 1
            if coord.y > env.dimension.y:
                coord.y = env.min_height
                print("BLOCKED")
                break

        return coord

    def generate_agents(self, t: int, environment: "Environment") -> List["PathAgent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):

            start = self.generate_stop_coordinate(self.stops[0], environment, t, self.near_radius)

            stays: List[int] = []
            locations: List["Coordinate4D"] = [start]
            total_travel_time: int = 0
            for stop in self.stops[1:]:
                next_location = self.generate_stop_coordinate(stop, environment, t, self.near_radius)

                stay = random.randint(0, 100)
                stays.append(stay)
                distance = locations[-1].distance(next_location)
                travel_time = math.ceil(distance) * self.speed
                total_travel_time += travel_time
                next_location.t = min(locations[-1].t + travel_time + stay + random.randint(0, 100),
                                      environment.dimension.t)
                locations.append(next_location)
            stays.pop()
            agent = self.initialize_agent(locations, stays)
            res.append(agent)
            print(f"{agent} {' -> '.join([str(loc) for loc in locations])}")

        self.agents += res
        return res
