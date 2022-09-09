from typing import List

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
