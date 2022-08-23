import statistics
from abc import ABC
from typing import Dict, List, TYPE_CHECKING

from .. import Blocker, Simulator, Statistics
from ..Agent import Agent, PathAgent, SpaceAgent
from ..Blocker.BuildingBlocker import BuildingBlocker
from ..Blocker.DynamicBlocker import DynamicBlocker
from ..Blocker.StaticBlocker import StaticBlocker
from ..History import HistoryAgent
from ..IO import Stringify
from ..Generator.MapTile import MapTile

if TYPE_CHECKING:
    from ..Coordinate import Coordinate4D
    from ..Path.AllocationReason import AllocationReason
    from API import APISimulationConfig


class Path(Stringify):
    def __init__(self, path: List["Coordinate4D"]):
        self.t: Dict[str, List[int, int, int]] = {}

        for coord in path:
            self.t[str(int(coord.t))] = [coord.x, coord.y, coord.z]


class Collision(Stringify):
    def __init__(self, reason: "AllocationReason", agent_id: int = -1, blocker_id: int = -1):
        self.reason: "AllocationReason" = reason
        self.agent_id: int = agent_id
        self.blocker_id: int = blocker_id


class Branch(Stringify):
    def __init__(self, tick: int, paths: List["Path"], value: float, reason: "Collision", compute_time: float):
        self.tick: int = tick
        self.paths: List["Path"] = paths
        self.value: float = value
        self.reason: "Collision" = reason
        self.compute_time = compute_time


class JSONAgent(ABC):
    def __init__(
        self,
        agent: Agent,
        non_colliding_utility: float,
        bid: Dict[str, str | int | float],
        owner_id: int,
        owner_name: str,
    ):
        self.agent_type: str = agent.agent_type
        self.allocation_type = agent.allocation_type
        self.id: int = agent.id
        self.utility: float = agent.get_allocated_value()

        self.non_colliding_utility: float = non_colliding_utility

        self.bid: Dict[str, str | int | float] = bid
        self.owner_id: int = owner_id
        self.owner_name: str = owner_name
        self.name: str = f"{self.owner_name}-{self.agent_type}-{self.id}"


class JSONSpaceAgent(JSONAgent, Stringify):
    def __init__(
        self,
        agent: SpaceAgent,
        non_colliding_utility: float,
        bid: Dict[str, str | int | float],
        owner_id: int,
        owner_name: str,
    ):
        super().__init__(agent, non_colliding_utility, bid, owner_id, owner_name)
        self.spaces = agent.get_allocated_segments()


class JSONPathAgent(JSONAgent, Stringify):
    def __init__(
        self,
        history_agent: HistoryAgent,
        agent: PathAgent,
        non_colliding_utility: float,
        near_field_intersections: int,
        far_field_intersections: int,
        near_field_violations: int,
        far_field_violations: int,
        bid: Dict[str, str | int | float],
        owner_id: int,
        owner_name: str,
        path_stats: Dict[str, float | int]
    ):
        super().__init__(agent, non_colliding_utility, bid, owner_id, owner_name)
        self.speed: int = agent.speed
        self.near_radius: int = agent.near_radius
        self.far_radius: int = agent.far_radius
        self.battery: int = agent.battery
        self.time_in_air: int = agent.get_airtime()

        self.near_field_intersections: int = near_field_intersections
        self.far_field_intersections: int = far_field_intersections
        self.near_field_violations: int = near_field_violations
        self.far_field_violations: int = far_field_violations

        self.paths: List[Path] = [Path(path.coordinates) for path in agent.get_allocated_segments()]

        self.branches: List[Branch] = []

        self.average_height = path_stats["avg_height"]
        self.median_height = path_stats["med_height"]
        self.ascend = path_stats["asc"]
        self.descend = path_stats["desc"]
        self.distance = path_stats["dist"]
        self.nr_reallocations = len(self.branches)

        for key, value in list(history_agent.past_allocations.items()):
            branch_paths = [Path(path) for path in value["path"]]
            self.branches.append(Branch(
                key,
                branch_paths,
                agent.value_for_segments(value["path"]),
                Collision(value["reason"]),
                value["time"]
            ))


class JSONOwner(Stringify):
    def __init__(self, name: str, _id: int, color: str, agents: List[JSONAgent]):
        self.name: str = name
        self.id: int = _id
        self.color: str = color
        self.agents: List[JSONAgent] = agents
        self.total_time_in_air: int = sum(
            [agent.time_in_air if isinstance(agent, JSONPathAgent) else 0 for agent in self.agents])

        bids = [agent.bid["!value"] for agent in self.agents]
        self.total_bid_value: int = sum(bids)
        self.mean_bid_value: float = statistics.mean(bids)
        self.median_bid_value: float = statistics.median(bids)
        self.max_bid_value: float = max(bids)
        self.min_bid_value: float = min(bids)
        if len(bids) < 2:
            self.bid_quantiles = [0] * 4
        else:
            self.bid_quantiles: List[float] = statistics.quantiles(bids)
        self.bid_outliers: List[float] = [bid for bid in bids if
                                          bid < self.bid_quantiles[0] or bid > self.bid_quantiles[-1]]

        utility = [agent.utility for agent in self.agents]
        self.total_utility: int = sum(utility)
        self.mean_utility: float = statistics.mean(utility)
        self.median_utility: float = statistics.median(utility)
        self.max_utility: float = max(utility)
        self.min_utility: float = min(utility)
        if len(utility) < 2:
            self.utility_quantiles = [0] * 4
        else:
            self.utility_quantiles: List[float] = statistics.quantiles(utility)
        self.utility_outliers: List[float] = [w for w in utility if
                                              w < self.utility_quantiles[0] or w > self.utility_quantiles[-1]]

        self.number_of_agents: int = len(self.agents)
        self.number_per_type = {}
        for agent in self.agents:
            self.number_per_type[agent.agent_type] = self.number_per_type.get(agent.agent_type, 0) + 1


class JSONBlocker(Stringify):
    def __init__(self, blocker: Blocker):
        self.id: int = blocker.id
        self.blocker_type = blocker.blocker_type
        if isinstance(blocker, DynamicBlocker):
            self.path: Path = Path(blocker.locations)
        elif isinstance(blocker, StaticBlocker):
            self.location = blocker.location
        self.dimension = blocker.dimension


class JSONMaptile(Stringify):
    def __init__(self, maptile: "MapTile"):
        self.x = maptile.x
        self.y = maptile.y
        self.z = maptile.z
        self.resolution = maptile.area.resolution


class JSONEnvironment(Stringify):
    def __init__(self, dimensions: "Coordinate4D", blockers: List[Blocker], maptiles: List[MapTile]):
        self.dimensions: "Coordinate4D" = dimensions
        self.blockers: List[JSONBlocker] = [JSONBlocker(blocker) for blocker in blockers if
                                            not isinstance(blocker, BuildingBlocker)]
        self.maptiles: List[JSONMaptile] = [JSONMaptile(maptile) for maptile in maptiles]


class JSONStatistics(Stringify):
    def __init__(self, nr_owners, nr_agens, achieved_welfare, nr_collisions, nr_reallocations):
        self.total_number_of_owners = nr_owners
        self.total_number_of_agents = nr_agens
        self.total_achieved_welfare = achieved_welfare
        self.total_number_of_collisions = nr_collisions
        self.total_number_of_reallocations = nr_reallocations


class JSONSimulation(Stringify):
    def __init__(self,
                 config: "APISimulationConfig",
                 environment: JSONEnvironment,
                 jsonStatistics: JSONStatistics,
                 owners: List[JSONOwner],
                 total_compute_time: float,
                 step_compute_time: Dict[int, float]):
        self.config = config
        self.environment: JSONEnvironment = environment
        self.statistics: JSONStatistics = jsonStatistics
        self.owners: List[JSONOwner] = owners
        self.compute_time = total_compute_time
        self.step_compute_time = step_compute_time


def build_json(config: "APISimulationConfig", simulator: Simulator, total_compute_time: float):
    env = simulator.environment
    history = simulator.history
    stats = Statistics(simulator)
    close_encounters = stats.close_encounters()
    nr_collisions = 0
    json_env = JSONEnvironment(env.get_dim(), list(env.blockers.values()), env.map_tiles)
    owners: List[JSONOwner] = []
    for owner in history.owners:
        agents: List[JSONAgent] = []
        non_colliding_values = calculate_non_colliding_values(owner.agents, stats)
        for agent in owner.agents:
            if isinstance(agent, PathAgent):
                path_stats = stats.path_statistics(agent.get_allocated_coords())
                agents.append(JSONPathAgent(
                    history.agents[agent],
                    agent,
                    non_colliding_values[agent],
                    close_encounters[agent.id]["total_near_field_intersection"],
                    close_encounters[agent.id]["total_far_field_intersection"],
                    close_encounters[agent.id]["total_near_field_violations"],
                    close_encounters[agent.id]["total_far_field_violations"],
                    agent.generalized_bid(),
                    owner.id,
                    owner.name,
                    path_stats,
                ))
            elif isinstance(agent, SpaceAgent):
                agents.append(JSONSpaceAgent(
                    agent,
                    stats.non_colliding_value(agent),
                    agent.generalized_bid(),
                    owner.id,
                    owner.name,
                ))
            nr_collisions += close_encounters[agent.id]["total_near_field_violations"]  # todo different collision metric
        owners.append(JSONOwner(owner.name, owner.id, owner.color, agents))
    json_stats = JSONStatistics(len(simulator.owners), len(env._agents), stats.total_agents_welfare(), nr_collisions, 0) # TODO reallocations
    json_simulation = JSONSimulation(config, json_env, json_stats, owners, total_compute_time,
                                     history.compute_times)
    return json_simulation.as_dict()


def calculate_non_colliding_values(agents: List[Agent], stats: Statistics):
    res = {}
    # with Pool(len(agents)) as p: #ToDo: doesn't work idk
    #     non_colliding_values = p.map(lambda _agent: stats.non_colliding_value(_agent), agents)
    non_colliding_values_2 = []
    for agent in agents:
        non_colliding_values_2.append(stats.non_colliding_value(agent))
    for agent, non_colliding_value in zip(agents, non_colliding_values_2):
        res[agent] = non_colliding_value
    return res
