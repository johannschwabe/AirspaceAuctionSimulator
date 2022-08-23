from typing import TYPE_CHECKING, List, Optional

from .Allocation import Allocation

if TYPE_CHECKING:
    from .PathSegment import PathSegment
    from ..Agents.PathAgent import PathAgent


class PathAllocation(Allocation):
    def __init__(self,
                 agent: "PathAgent",
                 segments: List["PathSegment"],
                 reason: str,
                 compute_time: int = 0,
                 colliding_agents_ids: Optional[List[int]] = None):
        super().__init__(agent, segments, reason, compute_time=compute_time, colliding_agents_ids=colliding_agents_ids)
        self.agent: "PathAgent" = agent
        self.segments: List["PathSegment"] = segments

    def get_real_allocation(self, agent: "PathAgent"):
        return PathAllocation(agent, self.segments, self.reason, self.compute_time)
