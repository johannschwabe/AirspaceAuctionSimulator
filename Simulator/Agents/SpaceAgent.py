from typing import TYPE_CHECKING, List, Dict, Optional

from .Agent import Agent
from .AgentType import AgentType

if TYPE_CHECKING:
    from ..Segments.SpaceSegment import SpaceSegment
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..ValueFunction.ValueFunction import ValueFunction
    from ..Bids.BiddingStrategy import BiddingStrategy


class SpaceAgent(Agent):
    agent_type: str = AgentType.SPACE.value

    def __init__(self,
                 agent_id: str,
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction",
                 blocks: List[List["Coordinate4D"]],
                 config: Optional[Dict[str, object]] = None,
                 _is_clone: bool = False):
        super().__init__(agent_id, bidding_strategy, value_function, config, _is_clone=_is_clone)

        self.blocks: List[List["Coordinate4D"]] = blocks
        self.allocated_segments: List["SpaceSegment"] = []

    def add_allocated_segment(self, space_segment: "SpaceSegment"):
        self.allocated_segments.append(space_segment)

    def initialize_clone(self):
        clone = SpaceAgent(self.id, self.bidding_strategy, self.value_function, self.blocks,
                           config=self.config, _is_clone=True)
        return clone
