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

    def allocate_for_agent(self, agent: Agent, env: Environment) -> List[List[TimeCoordinate]]:
        bid: Bid = agent.get_bid()
        optimal_paths: List[List[TimeCoordinate]] = []

        # A-B
        if isinstance(bid, ABBid):
            ab_path = astar(
                bid.a,
                bid.b,
                env,
                agent.speed,
            )
            if len(ab_path) == 0 or ab_path[-1].t - ab_path[0].t > agent.battery:
                return []

            optimal_paths.append(ab_path)

            # A-B-A
            if isinstance(bid, ABABid):
                b = ab_path[-1]
                ba_path = astar(
                    TimeCoordinate(b.x, b.y, b.z, b.t + Tick(bid.stay)),
                    bid.a,
                    env,
                    agent.speed,
                )

                if len(ba_path) == 0 or ab_path[-1].t - ab_path[0].t + ba_path[-1].t - ba_path[0].t > agent.battery:
                    return []

                optimal_paths.append(ba_path)

        return optimal_paths
