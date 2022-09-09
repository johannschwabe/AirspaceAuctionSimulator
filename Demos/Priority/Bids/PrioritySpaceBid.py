from typing import List

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
