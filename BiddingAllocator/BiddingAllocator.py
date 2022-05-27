from typing import List, Dict

from Simulator.Path import PathSegment
from .BiddingABAgent import BiddingABAgent
from .BiddingABBid import BiddingABBid
from .BiddingPathFinding import bidding_astar
from Simulator import Environment, Tick
from Simulator.Agent import Agent
from Simulator.Allocator import Allocator
from Simulator.Coordinate import TimeCoordinate


class BiddingAllocator(Allocator):
    def __init__(self):
        super().__init__()

    def allocate_for_agents(self, agents: List[BiddingABAgent], env: Environment, tick: Tick) -> Dict[Agent, List[PathSegment]]:
        res = {}
        to_add = set(agents)
        while len(to_add) > 0:
            agent = max(to_add, key=lambda _agent: _agent.get_bid(tick).priority)
            to_add.remove(agent)
            bid = agent.get_bid(tick)
            if isinstance(bid, BiddingABBid):
                ab_path, collisions = bidding_astar(bid.a, bid.b, env, agent, bid.flying)
                new_path_segment = PathSegment(bid.a.to_inter_temporal(), bid.b.to_inter_temporal(), 0, ab_path)
                res[agent] = [new_path_segment]
                to_add = to_add.union(collisions)
                for agent_to_remove in collisions:
                    env.deallocate_agent(agent_to_remove, tick)
                env.allocate_path_segment_for_agent(agent, new_path_segment)
                if not agent.id in env.get_agents():
                    env.add_agent(agent)
        return res
