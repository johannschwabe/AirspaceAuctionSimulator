from typing import TYPE_CHECKING

from .Allocation import Allocation
from ..Agent.SpaceAgent import SpaceAgent

if TYPE_CHECKING:
    from .AllocationReason import AllocationReason
    from . import SpaceSegment
    from ..Agent.Agent import Agent


class SpaceAllocation(Allocation):
    def __init__(self,
                 agent: "SpaceAgent",
                 segments: list["SpaceSegment"],
                 reason: "AllocationReason",
                 compute_time: float = 0):
        super().__init__(agent, reason, compute_time)
        self.segments = segments

    def correct_agent(self, agent: "Agent"):
        if isinstance(agent, SpaceAgent):
            return SpaceAllocation(agent, self.segments, self.reason, self.compute_time)
        raise Exception("Invalid Agent Type")
