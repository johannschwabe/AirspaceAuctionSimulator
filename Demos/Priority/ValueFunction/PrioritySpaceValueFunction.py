from typing import List, TYPE_CHECKING

from Simulator import ValueFunction

if TYPE_CHECKING:
    from Simulator import SpaceAgent, Segment


class PrioritySpaceValueFunction(ValueFunction):
    label = "PrioSpace"
    description = "Magic"

    def value_for_segments(self, segments: List["Segment"], agent: "SpaceAgent"):
        sum_segments = 0.0
        for segment in segments:
            sum_segments += segment.nr_voxels

        sum_blocks = 0.0
        for block in agent.blocks:
            sum_blocks += block.nr_voxels

        return sum_segments * 0.0002 * (1 + agent.config["priority"] / 5) - (
                (sum_blocks - sum_segments) * agent.config["priority"] * 0.00002 * (1 + agent.config["priority"] / 10))
