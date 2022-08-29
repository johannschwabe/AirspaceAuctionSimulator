from typing import Optional, TYPE_CHECKING, List, Dict

from ..Agents.Agent import Agent
from ..Agents.AgentType import AgentType

if TYPE_CHECKING:
    from ..ValueFunction.ValueFunction import ValueFunction
    from ..Segments.PathSegment import PathSegment
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Bids.BiddingStrategy import BiddingStrategy


class PathAgent(Agent):
    DEFAULT_NEAR_RADIUS = 1
    DEFAULT_SPEED = 1
    DEFAULT_BATTERY = 100_000

    agent_type: str = AgentType.PATH.value

    def __init__(self,
                 agent_id: str,
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction",
                 locations: List["Coordinate4D"],
                 stays: List[int],
                 config: Optional[Dict[str, object]] = None,
                 speed: Optional[int] = None,
                 battery: Optional[int] = None,
                 near_radius: Optional[int] = None,
                 _is_clone: bool = False):

        super().__init__(agent_id, bidding_strategy, value_function, config, _is_clone=_is_clone)

        self.locations: List["Coordinate4D"] = locations
        self.stays: List[int] = stays

        self.speed: int = speed if speed is not None else self.DEFAULT_SPEED
        self.battery: int = battery if battery is not None else self.DEFAULT_BATTERY
        self.near_radius = near_radius if near_radius is not None else self.DEFAULT_NEAR_RADIUS

        self.allocated_segments: List["PathSegment"] = []

    def get_position_at_tick(self, tick: int):
        for segment in self.allocated_segments:
            if segment.max.t >= tick >= segment.min.t:
                index = tick - segment.min.t
                return segment.coordinates[index]
        return None

    def initialize_clone(self):
        clone = PathAgent(self.id,
                          self.bidding_strategy,
                          self.locations,
                          self.stays,
                          config=self.config,
                          speed=self.speed,
                          battery=self.battery,
                          near_radius=self.near_radius,
                          _is_clone=True)
        return clone

    def get_airtime(self) -> int:
        airtime = 0
        for path_segment in self.allocated_segments:
            airtime += path_segment.max.t - path_segment.min.t
        return airtime

    def add_allocated_segment(self, path_segment: "PathSegment"):
        if len(self.allocated_segments) > 0 and self.allocated_segments[-1].same(path_segment):
            self.allocated_segments[-1].join(path_segment)
        else:
            self.allocated_segments.append(path_segment)

    def get_allocated_coords(self) -> List["Coordinate4D"]:
        return [coord for path_segment in self.allocated_segments for coord in path_segment.coordinates]

    def does_collide(self, other_coordinate: "Coordinate4D", other_agent: "PathAgent"):
        min_t = other_coordinate.t
        max_t = other_coordinate.t + other_agent.speed
        for segment in self.allocated_segments:
            if segment.max.t >= min_t and segment.min.t <= max_t:
                min_index = max(min_t - segment.min.t, 0)
                max_index = min(max_t - segment.min.t, len(segment.coordinates) - 1)
                for coordinate in segment.coordinates[min_index:max_index]:
                    distance = coordinate.inter_temporal_distance(other_coordinate)
                    if distance == 0:
                        return True
                    if distance < self.near_radius or distance < other_agent.near_radius:
                        return True
        return False
