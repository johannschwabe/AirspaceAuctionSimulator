import statistics
from enum import Enum
from typing import Dict, List

from .. import Blocker, Simulator, Statistics
from ..Agent import Agent, AgentType
from ..History import HistoryAgent
from ..IO import Stringify
from ..Generator.MapTile import MapTile


class Path(Stringify):
    def __init__(self, path: List["TimeCoordinate"]):
        self.t: Dict[str, List[int, int, int]] = {}

        for coord in path:
            self.t[str(int(coord.t))] = [coord.x, coord.y, coord.z]


class Collision(Stringify):
    def __init__(self, reason: "Reason", agent_id: int = -1, blocker_id: int = -1):
        self.reason: "Reason" = reason
        self.agent_id: int = agent_id
        self.blocker_id: int = blocker_id


class Branch(Stringify):
    def __init__(self, tick: int, paths: List["Path"], value: float, reason: "Collision"):
        self.tick: int = tick
        self.paths: List["Path"] = paths
        self.value: float = value
        self.reason: "Collision" = reason


class Reason(Enum):
    AGENT = 1
    BLOCKER = 2
    OWNER = 3
    NOT_IMPLEMENTED = 4


class JSONAgent(Stringify):
    def __init__(
        self,
        history_agent: HistoryAgent,
        agent: Agent,
        non_colliding_welfare: float,
        near_field_intersections: int,
        far_field_intersections: int,
        near_field_violations: int,
        far_field_violations: int,
        bid: int,
        owner_id: int,
        owner_name: str,
    ):
        self.agent_type: AgentType = agent.agent_type
        self.id: int = agent.id
        self.speed: int = agent.speed
        self.near_radius: int = agent.near_radius
        self.far_radius: int = agent.far_radius
        self.welfare: float = agent.get_allocated_value()
        self.battery: int = agent.battery
        self.time_in_air: int = agent.get_airtime()

        self.non_colliding_welfare: float = non_colliding_welfare
        self.near_field_intersections: int = near_field_intersections
        self.far_field_intersections: int = far_field_intersections
        self.near_field_violations: int = near_field_violations
        self.far_field_violations: int = far_field_violations

        self.bid: int = bid
        self.owner_id: int = owner_id
        self.owner_name: str = owner_name
        self.name: str = f"{self.owner_name}-{self.agent_type.name}-Agent-{self.id}"

        self.paths: List[Path] = [Path(path) for path in agent.get_allocated_paths()]

        self.branches: List[Branch] = []

        res = find_flown_path(list(history_agent.past_allocations.values()))

        # First reallocation isn't a reallocation but an allocation
        for key, value in list(history_agent.past_allocations.items())[1:]:
            branch_paths = [Path(path) for path in value]
            self.branches.append(Branch(
                key,
                branch_paths,
                agent.value_for_paths(value),
                Collision(Reason.NOT_IMPLEMENTED)
            ))

def find_flown_path(reallocations):
    res = reallocations[-1]
    for allocation_index in range(len(reallocations) - 1, 0, -1):  # DER CODE IST SELBSTERKLÄREND
        path = reallocations[allocation_index]
        previous_allocation = reallocations[allocation_index - 1]

        if len(path[0]) == 0:
            print("send help")
            continue
        start_location = path[0][0]
        nr_stops = len(path)
        search_path = previous_allocation[-nr_stops]
        reallocation_index = start_location.t - search_path[0].t
        res[0] = search_path[0:reallocation_index] + res[0]
        if len(previous_allocation) > nr_stops:
            res = previous_allocation[0:-nr_stops] + res

    return res

class JSONOwner(Stringify):
    def __init__(self, name: str, id: int, color: str, agents: List[JSONAgent]):
        self.name: str = name
        self.id: int = id
        self.color: str = color
        self.agents: List[JSONAgent] = agents
        self.total_time_in_air: int = sum([agent.time_in_air for agent in self.agents])

        bids = [agent.bid for agent in self.agents]
        self.total_bid_value: int = sum(bids)
        self.mean_bid_value: float = statistics.mean(bids)
        self.median_bid_value: float = statistics.median(bids)
        self.max_bid_value: float = max(bids)
        self.min_bid_value: float = min(bids)
        self.bid_quantiles: List[float] = statistics.quantiles(bids)
        self.bid_outliers: List[float] = [bid for bid in bids if
                                          bid < self.bid_quantiles[0] or bid > self.bid_quantiles[-1]]

        welfare = [agent.welfare for agent in self.agents]
        self.total_welfare: int = sum(welfare)
        self.mean_welfare: float = statistics.mean(welfare)
        self.median_welfare: float = statistics.median(welfare)
        self.max_welfare: float = max(welfare)
        self.min_welfare: float = min(welfare)
        self.welfare_quantiles: List[float] = statistics.quantiles(welfare)
        self.welfare_outliers: List[float] = [w for w in welfare if
                                              w < self.welfare_quantiles[0] or w > self.welfare_quantiles[-1]]

        self.number_of_agents: int = len(self.agents)
        self.number_of_ab_agents: int = sum([int(agent.agent_type == AgentType.AB) for agent in self.agents])
        self.number_of_aba_agents: int = sum([int(agent.agent_type == AgentType.ABA) for agent in self.agents])
        self.number_of_abc_agents: int = sum([int(agent.agent_type == AgentType.ABC) for agent in self.agents])
        self.number_of_stationary_agents: int = sum(
            [int(agent.agent_type == AgentType.STATIONARY) for agent in self.agents])


class JSONBlocker(Stringify):
    def __init__(self, blocker: Blocker):
        self.id: int = blocker.id
        self.path: Path = Path(blocker.locations)
        self.dimension = blocker.dimension


class JSONMaptile(Stringify):
    def __init__(self, maptile: "MapTile"):
        self.x = maptile.x
        self.y = maptile.y
        self.z = maptile.z
        self.dimensions = maptile.dimensions
        self.top_left_coordinate = maptile.top_left_coordinate
        self.bottom_right_coordinate = maptile.bottom_right_coordinate


class JSONEnvironment(Stringify):
    def __init__(self, dimensions: "TimeCoordinate", blockers: List[Blocker], maptiles: List[MapTile]):
        self.dimensions: "TimeCoordinate" = dimensions
        self.blockers: List[JSONBlocker] = [JSONBlocker(blocker) for blocker in blockers]
        self.maptiles: List[JSONMaptile] = [JSONMaptile(maptile) for maptile in maptiles]


class JSONStatistics(Stringify):
    def __init__(self, nr_owners, nr_agens, achieved_welfare, nr_collisions, nr_reallocations):
        self.total_number_of_owners = nr_owners
        self.total_number_of_agents = nr_agens
        self.total_achieved_welfare = achieved_welfare
        self.total_number_of_collisions = nr_collisions
        self.total_number_of_reallocations = nr_reallocations


class JSONSimulation(Stringify):
    def __init__(self, name: str, description: str, environment: JSONEnvironment, statistics: JSONStatistics,
                 owners: List[JSONOwner]):
        self.name: str = name
        self.description: str = description
        self.environment: JSONEnvironment = environment
        self.statistics: JSONStatistics = statistics
        self.owners: List[JSONOwner] = owners


def build_json(simulator: Simulator, name: str, description: str):
    env = simulator.environment
    history = simulator.history
    stats = Statistics(simulator)
    # close_passings = stats.close_passings()
    nr_collisions = 0
    json_env = JSONEnvironment(env._dimension, env.blockers, env.map_tiles)
    owners: List[JSONOwner] = []
    for owner in history.owners:
        agents: List[JSONAgent] = []
        for agent in owner.agents:
            agents.append(JSONAgent(
                history.agents[agent],
                agent,
                stats.non_colliding_value(agent),
                # close_passings[agent.id]["total_near_field_intersection"],
                # close_passings[agent.id]["total_far_field_intersection"],
                # close_passings[agent.id]["total_near_field_violations"],
                # close_passings[agent.id]["total_far_field_violations"],
                0,
                0,
                0,
                0,
                0,
                owner.id,
                owner.name,
            ))
            # nr_collisions += close_passings[agent.id]["total_near_field_violations"]  # todo different collision metric
        owners.append(JSONOwner(owner.name, owner.id, owner.color, agents))
    json_stats = JSONStatistics(len(simulator.owners), len(env._agents), stats.total_agents_welfare(), nr_collisions, 0)
    json_simulation = JSONSimulation(name, description, json_env, json_stats, owners)
    return json_simulation.as_dict()
