from enum import Enum

from .. import Environment
from ..Allocator import Allocator
from ..History import HistoryAgent, History
from ..IO import Stringify
from ..Simulator import Owner
from ..Simulator import Simulator
from ..Agent import Agent, AgentType
from typing import List, TYPE_CHECKING

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
        non_colliding_value: float,
        near_field_intersections: int,
        far_field_intersections: int,
        near_field_violations: int,
        far_field_violations: int,
        bid: int,
    ):
        self.agent_type: AgentType = agent.agent_type
        self.speed: int = agent.speed
        self.id: int = agent.id
        self.near_radius: int = agent.near_radius
        self.far_radius: int = agent.far_radius
        self.value: float = agent.get_allocated_value()
        self.battery: int = agent.battery
        self.time_in_air: int = agent.get_airtime()

        self.non_colliding_value: float = non_colliding_value
        self.near_field_intersections: int = near_field_intersections
        self.far_field_intersections: int = far_field_intersections
        self.near_field_violations: int = near_field_violations
        self.far_field_violations: int = far_field_violations

        self.bid = bid

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
    def __init__(self, name: str, agents: List[JSONAgent]):
        self.name: str = name
        self.agents: List[JSONAgent] = agents


class JSONSimulation(Stringify):
    def __init__(self, name: str, description: str, owners: List[JSONOwner]):
        self.name: str = name
        self.description: str = description
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
                    -1
                ))
            owners.append(JSONOwner(owner.name, agents))
        json_simulation = JSONSimulation(self.name, self.description, owners)
        return json_simulation.as_dict()
