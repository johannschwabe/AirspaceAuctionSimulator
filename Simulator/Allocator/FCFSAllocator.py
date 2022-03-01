from typing import List

from ..Environment import Environment
from ..Agent import Agent
from ..Allocator import Allocator
from ..Bid import AToBBid, Bid
from ..Coordinate import TimeCoordinate
from ..helpers.PathFinding import astar


class FCFSAllocator(Allocator):
    def __init__(self):
        super().__init__()

    def allocate_for_agent(self, agent: Agent, env: Environment):
        bid: Bid = agent.get_bid()
        optimal_path: List[TimeCoordinate] = []
        if isinstance(bid, AToBBid):
            optimal_path = astar(
                bid.a,
                bid.b,
                env,
                agent.speed
            )

        return optimal_path
