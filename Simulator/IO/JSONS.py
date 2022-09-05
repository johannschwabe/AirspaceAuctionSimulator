from abc import ABC
from typing import Dict, List, TYPE_CHECKING, Union, Optional

from .Statistics import Statistics
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
    from ..Simulator import Simulator
    from ..Environment.Environment import Environment


class JSONPathSegment(Stringify):
    def __init__(self, path: "PathSegment"):
        self.t: Dict[str, List[int, int, int]] = {}

        for coord in path.coordinates:
            self.t[str(int(coord.t))] = [coord.x, coord.y, coord.z]


class JSONSpaceSegment(Stringify):
    def __init__(self, space: "SpaceSegment"):
        self.min = space.min
        self.max = space.max


class JSONAllocation(Stringify):
    def __init__(self, tick: int, paths: List["JSONPathSegment"], value: float, compute_time: int, reason: str,
                 colliding_agent_ids: Optional[List[str]]):
        self.tick: int = tick
        self.paths: List["JSONPathSegment"] = paths
        self.value: float = value
        self.reason: str = reason
        self.colliding_agent_ids: Optional[List[str]] = colliding_agent_ids
        self.compute_time: int = compute_time


class JSONAgent(ABC):
    def __init__(
        self,
        agent: "Agent",
        value: float,
        non_colliding_value: float,
    ):
        self.agent_type: str = agent.agent_type
        self.id: str = agent.id
        self.value: float = value

        self.non_colliding_value: float = non_colliding_value


class JSONSpaceAgent(JSONAgent, Stringify):
    def __init__(
        self,
        agent: "SpaceAgent",
        value: float,
        non_colliding_value: float,
    ):
        super().__init__(agent, value, non_colliding_value)
        self.spaces: List["JSONSpaceSegment"] = [JSONSpaceSegment(space) for space in agent.allocated_segments]


class JSONPathAgent(JSONAgent, Stringify):
    def __init__(
        self,
        agent: "PathAgent",
        value: float,
        non_colliding_value: float,
        branches: List["JSONAllocation"]
    ):
        super().__init__(agent, value, non_colliding_value)
        self.speed: int = agent.speed
        self.near_radius: int = agent.near_radius
        self.battery: int = agent.battery
        self.time_in_air: int = agent.get_airtime()

        self.path: List["JSONPathSegment"] = [JSONPathSegment(path) for path in agent.allocated_segments]
        self.branches = branches

        self.nr_reallocations = len(self.branches)


class JSONOwner(Stringify):
    def __init__(self,
                 owner: "Owner",
                 agents: List["JSONAgent"],
                 values: Dict[str, Union[float, List[float]]],
                 non_colliding_values: Dict[str, Union[float, List[float]]]):
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


def build_json(simulator: "Simulator", total_compute_time: int):
    """
    Build the JSON file of the simulation.
    :param simulator:
    :param total_compute_time:
    :return:
    """
    statistics = Statistics(simulator)
    json_simulation = statistics.get_json_simulation(total_compute_time)
    return json_simulation.as_dict()
