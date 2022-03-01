from typing import List

from ..Environment import Environment
from ..Agent import Agent
from ..Allocator import Allocator
from ..Bid import AToBBid, Bid
from ..Coordinate import TimeCoordinate
from ..Field import Field
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
                agent,
                env,
            )

        for coord in optimal_path:
            field: Field = env.get_field_at(coord, True)
            field.allocated_to = agent

        env.add_agent(agent)
        agent.allocated_path = optimal_path
