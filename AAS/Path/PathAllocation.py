from typing import TYPE_CHECKING, List

from .Allocation import Allocation

if TYPE_CHECKING:
    from ..Path.PathSegment import PathSegment
    from .AllocationReason import AllocationReason
    from ..Agents.PathAgents.PathAgent import PathAgent


class PathAllocation(Allocation):
    def __init__(self,
                 agent: "PathAgent",
                 segments: List["PathSegment"],
                 reason: "AllocationReason",
                 compute_time: int = 0):
        super().__init__(agent, segments, reason, compute_time)
        self.agent: "PathAgent" = agent
        self.segments: List["PathSegment"] = segments

    def correct_agent(self, agent: "PathAgent"):
        return PathAllocation(agent, self.segments, self.reason, self.compute_time)
