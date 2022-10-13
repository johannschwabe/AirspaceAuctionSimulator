from typing import List, Dict, Any, TYPE_CHECKING

from Simulator import Bid, SpaceAgent

if TYPE_CHECKING:
    from Simulator.Segments.SpaceSegment import SpaceSegment


class FCFSSpaceBid(Bid):
    def __init__(self, agent: "SpaceAgent", blocks: List["SpaceSegment"]):
        super().__init__(agent)
        # overwrite agent for typing
        self.agent: "SpaceAgent" = agent
        # requested blocks
        self.blocks: List["SpaceSegment"] = blocks

    def __gt__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __ge__(self, other):
        return True

    def __le__(self, other):
        return True

    def __eq__(self, other):
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": {
                "blocks": [{"min": [block.min.x, block.min.y, block.min.z, block.min.t],
                            "max": [block.max.x, block.max.y, block.max.z, block.max.t]} for block in self.blocks],
            },
            "display": {
                "area": "<br>".join([
                    f"min: {int(block.min.x)}, {int(block.min.y)}, {int(block.min.z)}, {block.min.t}, max: {int(block.max.x)}, {int(block.max.y)}, {int(block.max.z)}, {block.max.t}"
                    for block in self.blocks])
            }
        }
