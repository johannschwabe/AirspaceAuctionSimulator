from typing import Any, Dict, List, Optional, Set, TYPE_CHECKING

from .Agent import Agent
from .AgentType import AgentType

if TYPE_CHECKING:
    from ..Segments.SpaceSegment import SpaceSegment
    from ..ValueFunction.ValueFunction import ValueFunction
    from ..Bids.BiddingStrategy import BiddingStrategy


class SpaceAgent(Agent):
    agent_type: str = AgentType.SPACE.value

    def __init__(self,
                 agent_id: str,
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction",
                 blocks: List["SpaceSegment"],
                 config: Optional[Dict[str, Any]] = None,
                 _is_clone: bool = False):
        super().__init__(agent_id, bidding_strategy, value_function, config, _is_clone=_is_clone)

        self.blocks: List["SpaceSegment"] = blocks
        self.allocated_segments: List["SpaceSegment"] = []

    def add_allocated_segment(self, space_segment: "SpaceSegment"):
        for existing_segment in self.allocated_segments:
            if existing_segment.index == space_segment.index:
                assert existing_segment.min.inter_temporal_equal(space_segment.min)
                assert existing_segment.max.inter_temporal_equal(space_segment.max)
                assert existing_segment.max.t + 1 == space_segment.min.t
                existing_segment.max.t = space_segment.max.t
                print(
                    f"merged: {existing_segment.min},\n{existing_segment.max} \nfrom {space_segment.min},"
                    f"\n{space_segment.max}")
                return
        self.allocated_segments.append(space_segment)

    def get_segments_at_tick(self, tick: int) -> Set["SpaceSegment"]:
        segments = set()
        for segment in self.allocated_segments:
            if segment.max.t >= tick >= segment.min.t:
                segments.add(segment)
        return segments

    def get_segments_at_ticks(self, min_tick: int, max_tick: int) -> Set["SpaceSegment"]:
        segments = set()
        for tick in range(min_tick, max_tick + 1):  # Include upper bound
            segments.update(self.get_segments_at_tick(tick))
        return segments

    def initialize_clone(self):
        clone = SpaceAgent(self.id, self.bidding_strategy, self.value_function, self.blocks,
                           config=self.config, _is_clone=True)
        return clone
