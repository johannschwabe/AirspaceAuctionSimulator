from typing import List, TYPE_CHECKING, Optional

from .Agent import Agent
from .AgentType import AgentType
from .SpaceAgent import SpaceAgent
from ..Path import SpaceSegment
from ..Bid import Bid, StationaryBid

if TYPE_CHECKING:
    from ..Coordinate import Coordinate4D


class StationaryAgent(SpaceAgent):
    def __init__(
        self,
        blocks: List[List["Coordinate4D"]],
        agent_type: Optional[str] = None,
    ):
        if agent_type is None:
            agent_type = AgentType.STATIONARY.value

        super().__init__(agent_type)
        self.blocks: List[List["Coordinate4D"]] = blocks

    def value_for_segments(self, segments: List[SpaceSegment]) -> float:
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

    def get_bid(self, t: int) -> Bid:
        return StationaryBid(self.blocks)

    def clone(self):
        clone = StationaryAgent(self.blocks)
        clone.set_allocated_segments([segment.clone() for segment in self.get_allocated_segments()])
        clone.id = self.id
        clone.is_clone = True
        Agent._id -= 1

        return clone
