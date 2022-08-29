from typing import List, TYPE_CHECKING

from Simulator.ValueFunction.ValueFunction import ValueFunction

if TYPE_CHECKING:
    from Simulator.Agents.SpaceAgent import SpaceAgent
    from Simulator.Segments.Segment import Segment


class PrioritySpaceValueFunction(ValueFunction):
    def __init__(self):
        super().__init__(None)

    def value_for_segments(self, segments: List["Segment"], agent: "SpaceAgent"):
        sum_segments = 0.0
        for segment in segments:
            sum_segments += (segment.max.x - segment.min.x) * \
                            (segment.max.y - segment.min.y) * \
                            (segment.max.z - segment.min.z) * \
                            (segment.max.t - segment.min.t)
        sum_blocks = 0.0
        for block in agent.blocks:
            sum_blocks += (block[1].x - block[0].x) * \
                          (block[1].y - block[0].y) * \
                          (block[1].z - block[0].z) * \
                          (block[1].t - block[0].t)

        return sum_segments / sum_blocks
