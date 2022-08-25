from abc import ABC
from typing import TYPE_CHECKING, List

from .AllocationStatistics import AllocationStatistics
from ..Bids.Bid import Bid

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Segments.Segment import Segment


class Allocation(ABC):
    def __init__(self,
                 agent: "Agent",
                 segments: List["Segment"],
                 bid: Bid,
                 statistics: AllocationStatistics):
        self.agent: "Agent" = agent
        self.segments: List["Segment"] = segments
        self.bid: Bid = bid
        self.statistics = statistics
        self.payment = 0

    def get_real_allocation(self, agent: "Agent"):
        return Allocation(agent, self.segments, self.bid, self.statistics)

    @property
    def nr_voxels(self) -> int:
        count = 0
        for segment in self.segments:
            count += segment.nr_voxels
        return count
