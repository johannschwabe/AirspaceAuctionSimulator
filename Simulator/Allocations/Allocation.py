from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Segments.Segment import Segment


class Allocation(ABC):
    def __init__(self,
                 agent: "Agent",
                 segments: List["Segment"],
                 reason: str,
                 compute_time: int = 0,
                 colliding_agents_ids: Optional[List[int]] = None):
        self.agent: "Agent" = agent
        self.compute_time: int = compute_time
        self.segments: List["Segment"] = segments
        self.reason: str = reason
        self.colliding_agents_ids: Optional[List[int]] = colliding_agents_ids

    @abstractmethod
    def get_real_allocation(self, agent: "Agent"):
        pass
