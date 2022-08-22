from typing import TYPE_CHECKING, List

from .Allocation import Allocation

if TYPE_CHECKING:
    from ..Path.SpaceSegment import SpaceSegment
    from .AllocationReason import AllocationReason
    from ..Agents.SpaceAgents.SpaceAgent import SpaceAgent


class SpaceAllocation(Allocation):
    def __init__(self,
                 agent: "SpaceAgent",
                 segments: List["SpaceSegment"],
                 reason: "AllocationReason",
                 compute_time: int = 0):
        super().__init__(agent, segments, reason, compute_time)
        self.agent: "SpaceAgent" = agent
        self.segments: List["SpaceSegment"] = segments

    def get_real_allocation(self, agent: "SpaceAgent"):
        return SpaceAllocation(agent, self.segments, self.reason, self.compute_time)
