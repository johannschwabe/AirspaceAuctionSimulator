from abc import ABC
from typing import Dict, List, TYPE_CHECKING, Optional

from .Stringify import Stringify
from ..Agents.PathAgent import PathAgent
from ..Agents.SpaceAgent import SpaceAgent
from ..Blocker.BuildingBlocker import BuildingBlocker
from ..Blocker.DynamicBlocker import DynamicBlocker
from ..Blocker.StaticBlocker import StaticBlocker
from ..Owners.Owner import Owner

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Coordinates.Coordinate3D import Coordinate3D
    from ..Agents.Agent import Agent
    from ..Blocker.Blocker import Blocker
    from ..Segments.PathSegment import PathSegment
    from ..Segments.SpaceSegment import SpaceSegment
    from ..Environment.Environment import Environment


class PathStatistics(Stringify):
    def __init__(self,
                 l1_distance: int,
                 l2_distance: float,
                 l1_ground_distance: int,
                 l2_ground_distance: float,
                 height_difference: int,
                 time_difference: int,
                 ascent: int,
                 descent: int,
                 distance_traveled: int,
                 ground_distance_traveled: int,
                 mean_height: float,
                 median_height: int,
                 heights: List[int]):
        self.l1_distance: int = l1_distance
        self.l2_distance: float = l2_distance
        self.l1_ground_distance: int = l1_ground_distance
        self.l2_ground_distance: float = l2_ground_distance
        self.height_difference: int = height_difference
        self.time_difference: int = time_difference
        self.ascent: int = ascent
        self.descent: int = descent
        self.distance_traveled: int = distance_traveled
        self.ground_distance_traveled: int = ground_distance_traveled
        self.mean_height: float = mean_height
        self.median_height: int = median_height
        self.heights: List[int] = heights


class SpaceSegmentStatistics(Stringify):
    def __init__(self,
                 volume: int,
                 height: int,
                 area: int,
                 time: int,
                 height_above_ground: int):
        self.volume: int = volume
        self.height: int = height
        self.area: int = area
        self.time: int = time
        self.height_above_ground: int = height_above_ground


class SpaceStatistics(Stringify):
    def __init__(self,
                 volume: int,
                 mean_volume: float,
                 median_volume: int,
                 mean_height: float,
                 median_height: int,
                 area: int,
                 mean_area: float,
                 median_area: int,
                 mean_time: float,
                 median_time: int,
                 mean_height_above_ground: float,
                 median_height_above_ground: int):
        self.volume: int = volume
        self.mean_volume: float = mean_volume
        self.median_volume: int = median_volume
        self.mean_height: float = mean_height
        self.median_height: int = median_height
        self.area: int = area
        self.mean_area: float = mean_area
        self.median_area: int = median_area
        self.mean_time: float = mean_time
        self.median_time: int = median_time
        self.mean_height_above_ground: float = mean_height_above_ground
        self.median_height_above_ground: int = median_height_above_ground


class JSONPath(Stringify):
    def __init__(self, path_segment: "PathSegment"):
        self.positions: Dict[int, List[int, int, int]] = {}
        for coordinate in path_segment.coordinates:
            self.positions[coordinate.t] = [coordinate.x, coordinate.y, coordinate.z]


class JSONSpace(Stringify):
    def __init__(self, space: "SpaceSegment"):
        self.min = space.min
        self.max = space.max


class JSONBranch(Stringify):
    def __init__(self, tick: int, paths: List["JSONPath"], value: float, compute_time: int, reason: str,
                 colliding_agent_ids: Optional[List[str]]):
        self.tick: int = tick
        self.paths: List["JSONPath"] = paths
        self.value: float = value
        self.reason: str = reason
        self.colliding_agent_ids: List[str] = colliding_agent_ids if colliding_agent_ids is not None else []
        self.compute_time: int = compute_time


class JSONViolations(Stringify):
    def __init__(self,
                 violations: Dict[str, List["Coordinate4D"]],
                 total_violations: int):
        self.violations: Dict[str, List["Coordinate4D"]] = violations
        self.total_violations: int = total_violations


class JSONAgent(ABC):
    def __init__(
        self,
        agent: "Agent",
        value: float,
        non_colliding_value: float,
        violations: JSONViolations,
        total_reallocations: int,
    ):
        self.agent_type: str = agent.agent_type
        self.id: str = agent.id
        self.value: float = value
        self.non_colliding_value: float = non_colliding_value
        self.violations = violations
        self.total_reallocations = total_reallocations


class JSONSpaceAgent(JSONAgent, Stringify):
    def __init__(
        self,
        agent: "SpaceAgent",
        value: float,
        non_colliding_value: float,
        violations: JSONViolations,
        total_reallocations: int,
    ):
        super().__init__(agent, value, non_colliding_value, violations, total_reallocations)
        self.spaces: List["JSONSpace"] = [JSONSpace(space) for space in agent.allocated_segments]


class JSONPathAgent(JSONAgent, Stringify):
    def __init__(
        self,
        agent: "PathAgent",
        value: float,
        non_colliding_value: float,
        violations: JSONViolations,
        total_reallocations: int,
        branches: List["JSONBranch"],
    ):
        super().__init__(agent, value, non_colliding_value, violations, total_reallocations)
        self.speed: int = agent.speed
        self.near_radius: int = agent.near_radius
        self.battery: int = agent.battery
        self.time_in_air: int = agent.get_airtime()

        self.paths: List["JSONPath"] = [JSONPath(path) for path in agent.allocated_segments]
        self.branches = branches


class JSONValues(Stringify):
    def __init__(self,
                 values: List[float],
                 total: float,
                 mean: float,
                 median: float,
                 max_value: float,
                 min_value: float,
                 quartiles: List[float],
                 outliers: List[float]):
        self.values: List[float] = values
        self.total: float = total
        self.mean: float = mean
        self.median: float = median
        self.max: float = max_value
        self.min: float = min_value
        self.quartiles: List[float] = quartiles
        self.outliers: List[float] = outliers


class JSONOwner(Stringify):
    def __init__(self,
                 owner: "Owner",
                 agents: List["JSONAgent"],
                 values: JSONValues,
                 non_colliding_values: JSONValues):
        self.name: str = owner.name
        self.id: str = owner.id
        self.color: str = owner.color
        self.agents: List["JSONAgent"] = agents
        self.total_time_in_air: int = sum(
            [agent.time_in_air if isinstance(agent, JSONPathAgent) else 0 for agent in self.agents])

        self.values = values
        self.non_colliding_values = non_colliding_values

        self.number_of_agents: int = len(self.agents)
        self.number_per_type = {}
        for agent in self.agents:
            self.number_per_type[agent.agent_type] = self.number_per_type.get(agent.agent_type, 0) + 1


class JSONBlocker(Stringify):
    def __init__(self, blocker: "Blocker"):
        self.id: str = f"blocker-{blocker.id}"
        self.blocker_type = blocker.blocker_type
        if isinstance(blocker, DynamicBlocker):
            self.locations: List["Coordinate4D"] = blocker.locations
        elif isinstance(blocker, StaticBlocker):
            self.location: "Coordinate3D" = blocker.location
        self.dimension = blocker.dimension


class JSONEnvironment(Stringify):
    def __init__(self, environment: "Environment"):
        self.dimensions: "Coordinate4D" = environment.dimension
        self.blockers: List["JSONBlocker"] = [JSONBlocker(blocker) for blocker in environment.blocker_dict.values() if
                                              not isinstance(blocker, BuildingBlocker)]


class JSONStatistics(Stringify):
    def __init__(self, nr_owners: int, nr_agents: int, value: float, non_colliding_value: float, nr_collisions: int,
                 nr_reallocations: int):
        self.total_number_of_owners = nr_owners
        self.total_number_of_agents = nr_agents
        self.total_value = value
        self.total_non_colliding_value = non_colliding_value
        self.total_number_of_collisions = nr_collisions
        self.total_number_of_reallocations = nr_reallocations


class JSONSimulation(Stringify):
    def __init__(self,
                 environment: "JSONEnvironment",
                 jsonStatistics: "JSONStatistics",
                 owners: List["JSONOwner"],
                 total_compute_time: int,
                 step_compute_time: Dict[int, int]):
        self.environment: "JSONEnvironment" = environment
        self.statistics: "JSONStatistics" = jsonStatistics
        self.owners: List["JSONOwner"] = owners
        self.compute_time: int = total_compute_time
        self.step_compute_time: Dict[int, int] = step_compute_time
