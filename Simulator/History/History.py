from typing import List, Dict, TYPE_CHECKING

from .HistoryAgent import HistoryAgent

if TYPE_CHECKING:
    from ..Environment.Environment import Environment
    from ..Allocator.Allocator import Allocator
    from ..Agents.Agent import Agent
    from ..Owners.Owner import Owner
    from ..Path.Allocation import Allocation


class History:
    def __init__(self, allocator: "Allocator", env: "Environment", owners: List["Owner"]):
        self.agents: Dict["Agent", HistoryAgent] = {}
        self.owners: List["Owner"] = owners
        self.allocator: "Allocator" = allocator
        self.env: "Environment" = env
        self.compute_times: Dict[int, int] = {}

    def set_owners(self, owners: List["Owner"]):
        self.owners = owners

    def add_new_agents(self, agents: List["Agent"], time_step: int):
        for agent in agents:
            self.agents[agent] = HistoryAgent(agent, time_step)

    def update_allocations(self,
                           new_allocations: List["Allocation"],
                           time_step: int,
                           compute_time: int):
        self.compute_times[time_step] = compute_time
        for allocation in new_allocations:
            history_agent = self.agents[allocation.agent]
            history_agent.reallocation(allocation.segments, allocation.reason, time_step, allocation.compute_time)
