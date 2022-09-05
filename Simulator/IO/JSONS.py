from abc import ABC
from typing import Dict, List, TYPE_CHECKING, Union

from .Stringify import Stringify
from ..Agents.PathAgent import PathAgent
from ..Agents.SpaceAgent import SpaceAgent
from ..Blocker.BuildingBlocker import BuildingBlocker
from ..Blocker.DynamicBlocker import DynamicBlocker
from ..Blocker.StaticBlocker import StaticBlocker
from ..Owners.Owner import Owner
from ..Statistics.Statistics import Statistics

if TYPE_CHECKING:
    from ..Coordinates import Coordinate4D
    from ..Allocations.AllocationReason import AllocationReason
    from ..Agents.Agent import Agent
    from ..Blocker.Blocker import Blocker
    from ..Segments.PathSegment import PathSegment
    from ..Segments.SpaceSegment import SpaceSegment
    from ..Simulator import Simulator


class JSONPath(Stringify):
    def __init__(self, path: "PathSegment"):
        self.t: Dict[str, List[int, int, int]] = {}

        for coord in path.coordinates:
            self.t[str(int(coord.t))] = [coord.x, coord.y, coord.z]


class JSONSpace(Stringify):
    def __init__(self, space: "SpaceSegment"):
        self.min = space.min
        self.max = space.max


class JSONCollision(Stringify):
    def __init__(self, reason: "AllocationReason", agent_id: int = -1, blocker_id: int = -1):
        self.reason: "AllocationReason" = reason
        self.agent_id: int = agent_id
        self.blocker_id: int = blocker_id


class JSONBranch(Stringify):
    def __init__(self, tick: int, paths: List["JSONPath"], value: float, reason: "JSONCollision", compute_time: int):
        self.tick: int = tick
        self.paths: List["JSONPath"] = paths
        self.value: float = value
        self.reason: "JSONCollision" = reason
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
        self.spaces: List["JSONSpace"] = [JSONSpace(space) for space in agent.allocated_segments]


class JSONPathAgent(JSONAgent, Stringify):
    def __init__(
        self,
        agent: "PathAgent",
        value: float,
        non_colliding_value: float,
    ):
        super().__init__(agent, value, non_colliding_value)
        self.speed: int = agent.speed
        self.near_radius: int = agent.near_radius
        self.battery: int = agent.battery
        self.time_in_air: int = agent.get_airtime()

        self.paths: List["JSONPath"] = [JSONPath(path) for path in agent.allocated_segments]

        self.branches: List["JSONBranch"] = []

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
            self.location: "Coordinate4D" = blocker.location
        self.dimension = blocker.dimension


class JSONEnvironment(Stringify):
    def __init__(self, dimensions: "Coordinate4D", blockers: List["Blocker"]):
        self.dimensions: "Coordinate4D" = dimensions
        self.blockers: List["JSONBlocker"] = [JSONBlocker(blocker) for blocker in blockers if
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
    env = simulator.environment
    history = simulator.history
    stats = Statistics(simulator)
    json_env = JSONEnvironment(env.dimension, list(env.blocker_dict.values()))
    owners: List["JSONOwner"] = []
    for owner in simulator.owners:
        agents: List["JSONAgent"] = []
        for agent in owner.agents:
            if isinstance(agent, PathAgent):
                agents.append(JSONPathAgent(
                    agent,
                    stats.get_value_for_agent(agent),
                    stats.get_non_colliding_value_for_agent(agent),
                ))
            elif isinstance(agent, SpaceAgent):
                agents.append(JSONSpaceAgent(
                    agent,
                    stats.get_value_for_agent(agent),
                    stats.get_non_colliding_value_for_agent(agent),
                ))
        owners.append(JSONOwner(owner,
                                agents,
                                stats.get_values_for_owner(owner),
                                stats.get_non_colliding_values_for_owner(owner)))
    json_stats = JSONStatistics(len(simulator.owners), len(env.agents), stats.get_total_value(),
                                0)
    json_simulation = JSONSimulation(json_env, json_stats, owners, total_compute_time,
                                     history.compute_times)
    return json_simulation.as_dict()


def _calculate_non_colliding_values(agents: List["Agent"], stats: "Statistics") -> Dict["Agent", float]:
    """
    Calculate the non-colliding values for all agents.
    :param agents:
    :param stats:
    :return:
    """
    res = {}
    non_colliding_values = []
    for agent in agents:
        non_colliding_values.append(stats.get_non_colliding_value_for_agent(agent))
    for agent, non_colliding_value in zip(agents, non_colliding_values):
        res[agent] = non_colliding_value
    return res
