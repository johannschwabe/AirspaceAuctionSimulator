from abc import ABC
from typing import Optional, TYPE_CHECKING, List

from .Agent import Agent
from .AgentType import AgentType

if TYPE_CHECKING:
    from ..Allocation.SpaceSegment import SpaceSegment
    from ..Simulator import Simulator
    from ..Coordinates.Coordinate4D import Coordinate4D


class SpaceAgent(Agent, ABC):
    agent_type: str = AgentType.SPACE.value

    def __init__(self,
                 blocks: List[List["Coordinate4D"]],
                 simulator: "Simulator",
                 agent_id: Optional[int] = None):
        super().__init__(simulator, agent_id)

        self.blocks: List[List["Coordinate4D"]] = blocks
        self.allocated_segments: List["SpaceSegment"] = []

    def add_allocated_segment(self, space_segment: "SpaceSegment"):
        self.allocated_segments.append(space_segment)

    def value_for_segments(self, segments: List["SpaceSegment"]) -> float:
        sum_segments = 0.0
        for segment in segments:
            sum_segments += (segment.max.x - segment.min.x) * \
                            (segment.max.y - segment.min.y) * \
                            (segment.max.z - segment.min.z) * \
                            (segment.max.t - segment.min.t)
        sum_blocks = 0.0
        for block in self.blocks:
            sum_blocks += (block[1].x - block[0].x) * \
                          (block[1].y - block[0].y) * \
                          (block[1].z - block[0].z) * \
                          (block[1].t - block[0].t)

        return sum_segments / sum_blocks
