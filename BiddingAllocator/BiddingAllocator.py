from typing import List, Dict

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

    def allocate_for_agents(self, agents: List[BiddingABAgent], env: Environment, tick: Tick) -> Dict[Agent, List[List[TimeCoordinate]]]:
        res = {}
        to_add = set(agents)
        while len(to_add) > 0:
            agent = max(to_add, key=lambda _agent: _agent.get_bid().priority)
            to_add.remove(agent)
            bid = agent.get_bid()
            if isinstance(bid, BiddingABBid):
                ab_path, collisions = bidding_astar(bid.a, bid.b, env, agent)
                res[agent] = [ab_path]
                to_add.union(collisions)
                for agent_to_remove in collisions:
                    env.deallocate_agent(agent_to_remove, tick)
                env.allocate_path_for_agent(agent, ab_path)
                if not agent in env.get_agents():
                    env.add_agent(agent)
        return res
