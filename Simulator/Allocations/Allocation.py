from abc import ABC
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Segments.Segment import Segment
    from .AllocationStatistics import AllocationStatistics


class Allocation(ABC):
    """
    A new allocation for an agent. Can be done for agent clones or real agents.
    """

    def __init__(self, agent: "Agent", segments: List["Segment"], statistics: "AllocationStatistics"):
        """
        An allocation consists of an agent, the allocated segments,
        the payment (which is calculated later by the payment-rule) and some statistics.
        :param agent:
        :param segments:
        :param statistics:
        """
        self.agent: "Agent" = agent
        self.segments: List["Segment"] = segments
        self.statistics: "AllocationStatistics" = statistics
        self.payment = 0

    def get_allocation_with_agent(self, agent: "Agent") -> "Allocation":
        """
        Create a new allocation wich is a copy of this with the given agent.
        :param agent:
        :return:
        """
        return Allocation(agent, self.segments, self.statistics)

    @property
    def nr_voxels(self) -> int:
        """
        Return #voxels in all allocated segments.
        :return:
        """
        count = 0
        for segment in self.segments:
            count += segment.nr_voxels
        return count
