import json
from typing import List, Dict

from Simulator import Bid, SpaceAgent, Coordinate4D


class FCFSSpaceBid(Bid):
    def __init__(self, agent: "SpaceAgent", blocks: List[List["Coordinate4D"]]):
        super().__init__(agent)
        # overwrite agent for typing
        self.agent: "SpaceAgent" = agent
        # requested blocks
        self.blocks: List[List["Coordinate4D"]] = blocks

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

    def to_dict(self) -> Dict[str, str | int | float]:
        return {
            "blocks": json.dumps([{"min": [block[0].x, block[0].y, block[0].z, block[0].t],
                                   "max": [block[1].x, block[1].y, block[1].z, block[1].t]} for block in self.blocks]),
        }
