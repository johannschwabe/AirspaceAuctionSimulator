from abc import ABC
from typing import Dict, List, TYPE_CHECKING, Any

from .Stringify import Stringify
from .. import Simulator
from ..Agents.PathAgent import PathAgent
from ..Agents.SpaceAgent import SpaceAgent
from ..Allocations.Allocation import Allocation
from ..Blocker.BuildingBlocker import BuildingBlocker
from ..Blocker.DynamicBlocker import DynamicBlocker
from ..Blocker.StaticBlocker import StaticBlocker
from ..Owners.Owner import Owner
from ..Segments.PathSegment import PathSegment

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Coordinates.Coordinate3D import Coordinate3D
    from ..Agents.Agent import Agent
    from ..Blocker.Blocker import Blocker
    from ..Segments.SpaceSegment import SpaceSegment
    from ..Environment.Environment import Environment


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
    def __init__(self, tick: int, paths: List["JSONPath"]):
        self.tick: int = tick
        self.paths: List["JSONPath"] = paths


class JSONAgent(ABC):
    def __init__(
        self,
        agent: "Agent",
    ):
        self.agent_type: str = agent.agent_type
        self.id: str = agent.id


class JSONSpaceAgent(JSONAgent, Stringify):
    def __init__(
        self,
        agent: "SpaceAgent",
    ):
        super().__init__(agent)
        self.spaces: List["JSONSpace"] = [JSONSpace(space) for space in agent.allocated_segments]


class JSONPathAgent(JSONAgent, Stringify):
    def __init__(
        self,
        agent: "PathAgent",
        branches: List["JSONBranch"]
    ):
        super().__init__(agent)
        self.speed: int = agent.speed
        self.near_radius: int = agent.near_radius
        self.battery: int = agent.battery
        self.paths: List["JSONPath"] = [JSONPath(path) for path in agent.allocated_segments]
        self.branches = branches


class JSONOwner(Stringify):
    def __init__(self,
                 owner: "Owner",
                 agents: List["JSONAgent"]):
        self.name: str = owner.name
        self.id: str = owner.id
        self.color: str = owner.color
        self.agents: List["JSONAgent"] = agents


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
    def __init__(self, nr_owners: int, nr_agents: int, achieved_welfare: float, nr_collisions: int,
                 nr_reallocations: int):
        self.total_number_of_owners = nr_owners
        self.total_number_of_agents = nr_agents
        self.total_achieved_welfare = achieved_welfare
        self.total_number_of_collisions = nr_collisions
        self.total_number_of_reallocations = nr_reallocations


class JSONSimulation(Stringify):
    def __init__(self,
                 environment: "JSONEnvironment",
                 owners: List["JSONOwner"],
                 ):
        self.environment: "JSONEnvironment" = environment
        self.owners: List["JSONOwner"] = owners


def get_json_branches_path_agent(path_agent: "PathAgent",
                                 allocations: Dict["Agent", Dict[int, "Allocation"]]) -> List["JSONBranch"]:
    json_allocations: List["JSONBranch"] = []
    for tick, allocation in allocations[path_agent].items():
        json_path_segments: List["JSONPath"] = []
        for path_segment in allocation.segments:
            assert isinstance(path_segment, PathSegment)
            json_path_segments.append(JSONPath(path_segment))

        json_allocations.append(JSONBranch(tick, json_path_segments))
    return json_allocations


def get_json_owners(simulation: "Simulator"):
    json_owners: List["JSONOwner"] = []
    for owner in simulation.owners:
        json_agents: List["JSONAgent"] = []
        for agent in owner.agents:
            if isinstance(agent, PathAgent):
                branches: List["JSONBranch"] = get_json_branches_path_agent(agent, simulation.history.allocations)
                json_agents.append(JSONPathAgent(
                    agent,
                    branches
                ))

            elif isinstance(agent, SpaceAgent):
                json_agents.append(JSONSpaceAgent(
                    agent,
                ))

            else:
                raise Exception(f"Invalid Agent: {agent}")

        json_owners.append(JSONOwner(owner, json_agents))

    return json_owners


def build_json_simulation(simulation: "Simulator") -> "JSONSimulation":
    json_environment = JSONEnvironment(simulation.environment)
    json_owners = get_json_owners(simulation)
    return JSONSimulation(json_environment,
                          json_owners)


def get_simulation_dict(simulation: "Simulator") -> Dict[str, Any]:
    return build_json_simulation(simulation).as_dict()
