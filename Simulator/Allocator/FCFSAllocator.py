from typing import List

from ..Time import Tick
from ..Environment import Environment
from ..Agent import Agent
from ..Allocator import Allocator
from ..Bid import ABBid, Bid, ABABid
from ..Coordinate import TimeCoordinate
from ..helpers.PathFinding import astar


class FCFSAllocator(Allocator):
    def __init__(self):
        super().__init__()

    def allocate_for_agent(self, agent: Agent, env: Environment):
        bid: Bid = agent.get_bid()
        optimal_path: List[TimeCoordinate] = []

        # A-B
        if isinstance(bid, ABBid):
            optimal_path = astar(
                bid.a,
                bid.b,
                env,
                agent.speed,
            )

            # A-B-A
            if isinstance(bid, ABABid) and len(optimal_path) > 0:
                b = optimal_path[-1]
                ba_path = astar(
                    TimeCoordinate(b.x, b.y, b.z, b.t + Tick(bid.stay)),
                    bid.a,
                    env,
                    agent.speed,
                )

                optimal_path = optimal_path + ba_path

        return optimal_path
