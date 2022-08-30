from typing import List, Dict, TYPE_CHECKING

from .HistoryAgent import HistoryAgent

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Allocations.Allocation import Allocation


class History:
    def __init__(self):
        self.agents: Dict["Agent", "HistoryAgent"] = {}
        self.compute_times: Dict[int, int] = {}

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
            history_agent.reallocation(allocation.segments, allocation.statistics.reason, time_step,
                                       allocation.statistics.compute_time)
