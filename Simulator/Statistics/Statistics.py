from enum import Enum

from .. import Environment
from ..Allocator import Allocator
from ..Blocker import Blocker
from ..History import HistoryAgent, History
from ..IO import Stringify
from ..Simulator import Owner
from ..Simulator import Simulator
from ..Agent import Agent, AgentType
from typing import List, TYPE_CHECKING
import statistics

if TYPE_CHECKING:
    from ..Coordinate import TimeCoordinate


class Path(Stringify):
    def __init__(self, path: List["TimeCoordinate"]):
        self.x: List[int] = []
        self.y: List[int] = []
        self.z: List[int] = []
        self.t: List[int] = []

        for coord in path:
            self.x.append(coord.x)
            self.y.append(coord.y)
            self.z.append(coord.z)
            self.t.append(coord.t)


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
        self.speed: int = agent.speed
        self.id: int = agent.id
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

        self.bid = bid
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.name = f"{self.owner_name}-{self.agent_type.name}-Agent-{self.id}"

        self.paths: List[Path] = [Path(path) for path in agent.get_allocated_paths()]

        self.branches: List[Branch] = []
        for key, value in history_agent.past_allocations.items():
            branch_paths = [Path(path) for path in value]
            self.branches.append(Branch(
                key,
                branch_paths,
                agent.value_for_paths(value),
                Collision(Reason.NOT_IMPLEMENTED)
            ))


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
        self.x = [loc.x for loc in blocker.locations.values()]
        self.y = [loc.y for loc in blocker.locations.values()]
        self.z = [loc.z for loc in blocker.locations.values()]
        self.t = [loc.t for loc in blocker.locations.values()]
        self.dimension = blocker.dimension


class JSONEnvironment(Stringify):
    def __init__(self, dimensions: "TimeCoordinate", blockers: List[Blocker]):
        self.dimensions = dimensions
        self.blockers = [JSONBlocker(blocker) for blocker in blockers]


class JSONStatistics(Stringify):
    def __init__(self):
        self.total_number_of_owners = 11
        self.total_number_of_agents = 22
        self.total_achieved_welfare = 33
        self.total_number_of_collisions = 44
        self.total_number_of_reallocations = 55


class JSONSimulation(Stringify):
    def __init__(self, name: str, description: str, environment: JSONEnvironment, statistics: JSONStatistics,
                 owners: List[JSONOwner]):
        self.name: str = name
        self.description: str = description
        self.environment: JSONEnvironment = environment
        self.statistics: JSONStatistics = statistics
        self.owners: List[JSONOwner] = owners


class Statistics:
    def __init__(self, sim: Simulator, name: str, description: str):
        self.env: "Environment" = sim.environment
        self.allocator: "Allocator" = sim.allocator
        self.history: "History" = sim.history
        self.owners: List["Owner"] = sim.owners
        self.time_elapsed: int = sim.time_step
        self.name: str = name
        self.description: str = description

    def non_colliding_value(self, agent: Agent):
        local_agent = agent.clone()
        local_env = self.env.clear()
        paths = self.allocator.allocate_for_agents([local_agent], local_env)[local_agent]
        return local_agent.value_for_paths(paths)

    def non_colliding_values(self):
        for agent in self.env.get_agents().values():
            print(f"{agent}'s non colliding value: {self.non_colliding_value(agent)}, "
                  f"achieved value: {agent.get_allocated_value()}")

    @staticmethod
    def agents_welfare(agent: Agent):
        return agent.get_allocated_value()

    def average_agents_welfare(self):
        summed_welfare = 0
        for agent in self.env.get_agents().values():
            summed_welfare += Statistics.agents_welfare(agent)
        print(f"AAW: {summed_welfare / len(self.env.get_agents())}")
        return summed_welfare / len(self.env.get_agents())

    @staticmethod
    def owners_welfare(owner: Owner):
        summed_welfare = 0
        for agent in owner.agents:
            summed_welfare += Statistics.agents_welfare(agent)
        return summed_welfare

    def average_owners_welfare(self):
        summed_welfare = 0
        for owner in self.history.owners:
            summed_welfare += Statistics.owners_welfare(owner)
        print(f"AOW: {summed_welfare / len(self.history.owners)}")
        return summed_welfare / len(self.history.owners)

    def allocated_distance(self):
        length = 0
        for agent in self.env.get_agents():
            for path in agent.allocated_paths:
                length += len(path)
        return length

    def build_json(self):
        json_env = JSONEnvironment(self.env._dimension, self.env.blockers)
        json_stats = JSONStatistics()
        owners: List[JSONOwner] = []
        for owner in self.owners:
            agents: List[JSONAgent] = []
            for agent in owner.agents:
                agents.append(JSONAgent(
                    self.history.agents[agent],
                    agent,
                    self.non_colliding_value(agent),
                    0,
                    0,
                    0,
                    0,
                    -1,
                    owner.id,
                    owner.name,
                ))
            owners.append(JSONOwner(owner.name, owner.id, owner.color, agents))
        json_simulation = JSONSimulation(self.name, self.description, json_env, json_stats, owners)
        return json_simulation.as_dict()
