from typing import TYPE_CHECKING, List, Dict, Optional, Any

from .Agent import Agent
from .AgentType import AgentType

if TYPE_CHECKING:
    from ..Segments.SpaceSegment import SpaceSegment
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Bids.BiddingStrategy import BiddingStrategy


class SpaceAgent(Agent):
    agent_type: str = AgentType.SPACE.value

    def __init__(self,
                 agent_id: str,
                 bidding_strategy: "BiddingStrategy",
                 blocks: List[List["Coordinate4D"]],
                 config: Optional[Dict[str, Any]] = None,
                 _is_clone: bool = False):
        super().__init__(agent_id, bidding_strategy, config, _is_clone=_is_clone)

        self.blocks: List[List["Coordinate4D"]] = blocks
        self.allocated_segments: List["SpaceSegment"] = []

    def add_allocated_segment(self, space_segment: "SpaceSegment"):
        self.allocated_segments.append(space_segment)

    def initialize_clone(self):
        clone = SpaceAgent(self.id, self.bidding_strategy, self.blocks, config=self.config, _is_clone=True)
        return clone

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
