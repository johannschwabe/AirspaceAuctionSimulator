from abc import ABC
from typing import Optional, TYPE_CHECKING, List

from .Agent import Agent
from .AllocationType import AllocationType

if TYPE_CHECKING:
    from ..Path.SpaceSegment import SpaceSegment
    from ..Simulator import Simulator


class SpaceAgent(Agent, ABC):
    allocation_type: str = AllocationType.SPACE.value

    def __init__(self,
                 simulator: "Simulator",
                 agent_id: Optional[int] = None):
        super().__init__(simulator, agent_id)

        self.allocated_segments: List["SpaceSegment"] = []

    def add_allocated_segment(self, space_segment: "SpaceSegment"):
        self.allocated_segments.append(space_segment)
