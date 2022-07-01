from typing import List, Dict

from Simulator.Enum import Reason
from Simulator.Path import PathSegment, PathReallocation, SpaceSegment, SpaceReallocation
from .BiddingABAgent import BiddingABAgent
from .BiddingABBid import BiddingABBid
from .BiddingPathFinding import bidding_astar
from Simulator import Environment, Tick
from Simulator.Agent import Agent
from Simulator.Allocator import Allocator
from Simulator.Coordinate import TimeCoordinate
from .BiddingStationaryAgent import BiddingStationaryAgent
from .BiddingStationaryBid import BiddingStationaryBid


class BiddingAllocator(Allocator):
    def __init__(self):
        super().__init__()

    def allocate_for_agents(self, agents: List[BiddingABAgent], env: Environment, tick: Tick) -> list[PathReallocation]:
        res = []
        to_add = set(agents)
        while len(to_add) > 0:
            agent = max(to_add, key=lambda _agent: _agent.get_bid(tick).priority)
            to_add.remove(agent)
            bid = agent.get_bid(tick)
            if isinstance(bid, BiddingABBid):
                ab_path, collisions = bidding_astar(bid.a, bid.b, env, agent, bid.flying)
                new_path_segment = PathSegment(bid.a.to_inter_temporal(), bid.b.to_inter_temporal(), 0, ab_path)
                reallocation_reason = Reason.FIRST_ALLOCATION if agent in agents else Reason.AGENT
                res.append(PathReallocation(agent, [new_path_segment], reallocation_reason))
                to_add = to_add.union(collisions)
                for agent_to_remove in collisions:
                    print(f"reallocating: {agent_to_remove.id}")
                    env.deallocate_agent(agent_to_remove, tick)
                env.allocate_path_segment_for_agent(agent, new_path_segment)
                if agent.id not in env.get_agents():
                    env.add_agent(agent)
            if isinstance(bid, BiddingStationaryBid) and isinstance(agent, BiddingStationaryAgent):
                space_segments = []
                for block in bid.blocks:
                    intersecting_agents = env.intersect_box(block[0], block[1], False)
                    blocking_agents = set()
                    allocateable = True
                    for agent_id in intersecting_agents:
                        if agent_id == agent.id:
                            continue
                        colliding_agent = env.get_agent(agent_id)
                        if colliding_agent.priority < agent.priority:
                            blocking_agents.add(colliding_agent)
                        else:
                            allocateable = False
                            break
                    if allocateable:
                        space_segments.append(SpaceSegment(block[0], block[1]))
                        to_add = to_add.union(blocking_agents)
                        for agent_to_remove in blocking_agents:
                            print(f"reallocating: {agent_to_remove.id}")
                            env.deallocate_agent(agent_to_remove, tick)

                reallocation_reason = Reason.FIRST_ALLOCATION if agent in agents else Reason.AGENT
                env.allocate_spaces_for_agent(agent, space_segments)
                res.append(SpaceReallocation(agent, space_segments, reallocation_reason))
                if agent.id not in env.get_agents():
                    env.add_agent(agent)
        return res
