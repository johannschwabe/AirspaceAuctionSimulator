from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Segments.Segment import Segment
    from .AllocationHistory import AllocationHistory


class Allocation:
    """
    A new allocation for an agent. Can be done for agent clones or real agents.
    """

    def __init__(self, agent: "Agent", segments: List["Segment"], history: "AllocationHistory"):
        """
        An allocation consists of an agent, the allocated segments,
        the payment (which is calculated later by the payment-rule) and some statistics.
        :param agent:
        :param segments:
        :param history:
        """
        self.agent: "Agent" = agent
        self.segments: List["Segment"] = segments
        self.history: "AllocationHistory" = history
        self.preliminary_payment = 0

    def get_allocation_with_agent(self, agent: "Agent") -> "Allocation":
        """
        Create a new allocation wich is a copy of this with the given agent.
        :param agent:
        :return:
        """
        return Allocation(agent, self.segments, self.history)

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
