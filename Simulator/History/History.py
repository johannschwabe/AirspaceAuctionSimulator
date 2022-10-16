from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Allocations.Allocation import Allocation


class History:
    """
    Record values for statistical analysis.
    """

    def __init__(self):
        """
        Allocation per agent per tick.
        Compute-time per tick.
        Registration tick per agent.
        """
        self.allocations: Dict["Agent", Dict[int, "Allocation"]] = {}
        self.compute_times: Dict[int, int] = {}
        self.registrations: Dict["Agent", int] = {}
        self.reallocations: Dict["Agent", int] = {}
        self.total_reallocations = 0

    def update_history(self,
                       new_allocations: List["Allocation"],
                       time_step: int,
                       compute_time: int):
        """
        Update history.
        :param new_allocations:
        :param time_step:
        :param compute_time:
        :return:
        """
        self.compute_times[time_step] = compute_time
        for allocation in new_allocations:
            agent = allocation.agent
            if agent not in self.allocations:
                self.registrations[agent] = time_step
                self.allocations[agent] = {}
                self.reallocations[agent] = 0
            else:
                self.reallocations[agent] += 1
                self.total_reallocations += 1
            self.allocations[agent][time_step] = allocation
