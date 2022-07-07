from typing import List, Dict, TYPE_CHECKING

from .HistoryAgent import HistoryAgent

if TYPE_CHECKING:
    from ..Simulator import Environment
    from ..Agent import Agent
    from ..Allocator import Allocator
    from ..Owner import Owner


class History:
    def __init__(self, allocator: "Allocator", env: "Environment", owners: List["Owner"]):
        self.agents: Dict["Agent", HistoryAgent] = {}
        self.owners: List["Owner"] = owners
        self.allocator: "Allocator" = allocator
        self.env: "Environment" = env
        self.compute_times: Dict[int, float] = {}

    def set_owners(self, owners: List["Owner"]):
        self.owners = owners

    def add_new_agents(self, agents: List["Agent"], time_step: int):
        for agent in agents:
            self.agents[agent] = HistoryAgent(agent, time_step)

    def update_allocations(self,
                           new_allocations: List["PathReallocation | SpaceReallocation"],
                           time_step,
                           compute_time: float):
        self.compute_times[time_step] = compute_time
        for reallocation in new_allocations:
            history_agent = self.agents[reallocation.agent]
            history_agent.reallocation(reallocation.segments, reallocation.reason, time_step, reallocation.compute_time)
