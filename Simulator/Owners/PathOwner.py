import math
import random
from typing import List, TYPE_CHECKING

from ..Agents.AgentType import AgentType
from ..Owners.Owner import Owner

if TYPE_CHECKING:
    from ..Location.GridLocation import GridLocation
    from ..Environment.Environment import Environment
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Agents.PathAgent import PathAgent
    from ..Bids.BiddingStrategy import BiddingStrategy
    from ..ValueFunction.ValueFunction import ValueFunction


class PathOwner(Owner):
    allocation_type: str = AgentType.PATH.value
    min_locations = 2
    max_locations = 100
    meta = []

    def __init__(self, owner_id: str,
                 name: str,
                 color: str,
                 stops: List["GridLocation"],
                 creation_ticks: List[int],
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction"):
        super().__init__(owner_id, bidding_strategy, value_function, name, color)
        self.creation_ticks = creation_ticks
        self.stops = stops

    @staticmethod
    def generate_stop_coordinate(stop: "GridLocation", env: "Environment", t: int, near_radius: int) -> "Coordinate4D":
        coord = stop.generate_coordinates(env, t + 1)

        while coord.y < env.min_height or env.is_blocked_forever(coord, near_radius):
            coord.y += 1
            if coord.y > env.dimension.y:
                coord.y = env.min_height
                print("BLOCKED")
                break

        return coord

    def initialize_agent(self,
                         locations: List["Coordinate4D"],
                         stays: List[int],
                         speed: int,
                         battery: int,
                         near_radius: int) -> "PathAgent":
        agent_id: str = self.get_agent_id()
        return PathAgent(agent_id, self.bidding_strategy, self.value_function, locations, stays,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius)

    def generate_agents(self, t: int, environment: "Environment") -> List["PathAgent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            speed = 1
            near_radius = 1
            start = self.generate_stop_coordinate(self.stops[0], environment, t, near_radius)

            stays: List[int] = []
            locations: List["Coordinate4D"] = [start]
            total_travel_time: int = 0
            for stop in self.stops[1:]:
                next_location = self.generate_stop_coordinate(stop, environment, t, near_radius)

                stay = random.randint(0, 100)
                stays.append(stay)
                distance = locations[-1].inter_temporal_distance(next_location)
                travel_time = math.ceil(distance) * speed
                total_travel_time += travel_time
                next_location.t = min(locations[-1].t + travel_time + stay + random.randint(0, 100),
                                      environment.dimension.t)
                locations.append(next_location)

            battery = total_travel_time * 4
            agent = self.initialize_agent(locations, stays, speed, battery, near_radius)
            res.append(agent)
            print(f"{agent} {' -> '.join([str(loc) for loc in locations])}")

        self.agents += res
        return res
