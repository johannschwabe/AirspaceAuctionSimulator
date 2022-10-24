from typing import List, Dict, Any, TYPE_CHECKING

from Simulator import Bid, SpaceAgent

if TYPE_CHECKING:
    from Simulator.Segments.SpaceSegment import SpaceSegment


class PrioritySpaceBid(Bid):
    def __init__(self, agent: "SpaceAgent", blocks: List["SpaceSegment"], priority: float):
        super().__init__(agent)
        # overwrite agent for typing
        self.agent: "SpaceAgent" = agent
        # requested blocks
        self.blocks: List["SpaceSegment"] = blocks
        # priority in collisions
        self.priority: float = priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": {
                "blocks": [{"min": [block.min.x, block.min.y, block.min.z, block.min.t],
                            "max": [block.max.x, block.max.y, block.max.z, block.max.t]} for block in self.blocks],
                "priority": self.priority
            },
            "display": {
                "area": "<br>".join([
                    f"min: {int(block.min.x)}, {int(block.min.y)}, {int(block.min.z)}, {block.min.t}, max: {int(block.max.x)}, {int(block.max.y)}, {int(block.max.z)}, {block.max.t}"
                    for block in self.blocks]),
                "priority": self.priority
            }
        }
