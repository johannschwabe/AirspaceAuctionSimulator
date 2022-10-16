from typing import List, TYPE_CHECKING

from Simulator import ValueFunction

if TYPE_CHECKING:
    from Simulator import SpaceAgent, Segment


class FCFSSpaceValueFunction(ValueFunction):
    label = "FCFS Space Value Function"
    description = "Allocated Voxel / Requested Voxel"

    def value_for_segments(self, segments: List["Segment"], agent: "SpaceAgent"):
        sum_segments = 0.0
        for segment in segments:
            sum_segments += (segment.max.x - segment.min.x) * \
                            (segment.max.y - segment.min.y) * \
                            (segment.max.z - segment.min.z) * \
                            (segment.max.t - segment.min.t)
        sum_blocks = 0.0
        for block in agent.blocks:
            sum_blocks += (block.max.x - block.min.x) * \
                          (block.max.y - block.min.y) * \
                          (block.max.z - block.min.z) * \
                          (block.max.t - block.min.t)

        return sum_segments / sum_blocks
