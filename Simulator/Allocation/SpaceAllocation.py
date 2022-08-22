from typing import TYPE_CHECKING, List, Optional

from .Allocation import Allocation

if TYPE_CHECKING:
    from ..Allocation.SpaceSegment import SpaceSegment
    from ..Agents.SpaceAgents.SpaceAgent import SpaceAgent


class SpaceAllocation(Allocation):
    def __init__(self,
                 agent: "SpaceAgent",
                 segments: List["SpaceSegment"],
                 reason: str,
                 compute_time: int = 0,
                 colliding_agents_ids: Optional[List[int]] = None):
        super().__init__(agent, segments, reason, compute_time=compute_time, colliding_agents_ids=colliding_agents_ids)
        self.agent: "SpaceAgent" = agent
        self.segments: List["SpaceSegment"] = segments

    def get_real_allocation(self, agent: "SpaceAgent"):
        return SpaceAllocation(agent, self.segments, self.reason, self.compute_time)
