from typing import TYPE_CHECKING

from .Allocation import Allocation
from ..Agent.PathAgent import PathAgent

if TYPE_CHECKING:
    from ..Path import PathSegment
    from .AllocationReason import AllocationReason
    from ..Agent.Agent import Agent


class PathAllocation(Allocation):
    def __init__(self,
                 agent: "PathAgent",
                 segments: list["PathSegment"],
                 reason: "AllocationReason",
                 compute_time: float = 0):
        super().__init__(agent, reason, compute_time)
        self.segments = segments

    def correct_agent(self, agent: "Agent"):
        if isinstance(agent, PathAgent):
            return PathAllocation(agent, self.segments, self.reason, self.compute_time)
        raise Exception("Invalid Agent Type")
