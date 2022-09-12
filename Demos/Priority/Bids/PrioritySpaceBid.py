import json
from typing import List, Dict

from Simulator import Bid, SpaceAgent, Coordinate4D


class PrioritySpaceBid(Bid):
    def __init__(self, agent: "SpaceAgent", blocks: List[List["Coordinate4D"]], priority: float):
        super().__init__(agent)
        # overwrite agent for typing
        self.agent: "SpaceAgent" = agent
        # requested blocks
        self.blocks: List[List["Coordinate4D"]] = blocks
        # priority in collisions
        self.priority: float = priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def to_dict(self) -> Dict[str, str | int | float]:
        return {
            "blocks": json.dumps([{"min": [block[0].x, block[0].y, block[0].z, block[0].t],
                                   "max": [block[1].x, block[1].y, block[1].z, block[1].t]} for block in self.blocks]),
            "priority": self.priority,
        }
