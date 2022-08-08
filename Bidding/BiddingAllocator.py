from time import time_ns
from typing import List, TYPE_CHECKING

from .BiddingABAgent import BiddingABAgent
from .BiddingABBid import BiddingABBid
from .BiddingABOwner import BiddingABOwner
from .BiddingAStar import BiddingAStar
from .BiddingStationaryAgent import BiddingStationaryAgent
from .BiddingStationaryBid import BiddingStationaryBid
from .BiddingStationaryOwner import BiddingStationaryOwner
from Simulator.Allocator import Allocator
from Simulator.Path import PathReallocation, PathSegment, SpaceSegment, SpaceReallocation
from Simulator.Path.AllocationReason import AllocationReason
from Simulator.Path.Reason import Reason

if TYPE_CHECKING:
    from Simulator import Environment


class BiddingAllocator(Allocator):
    @staticmethod
    def compatible_owner():
        return [BiddingABOwner, BiddingStationaryOwner]

    def __init__(self):
        super().__init__()

    def allocate_for_agents(self,
                            agents: List["BiddingABAgent"],
                            env: "Environment",
                            tick: int) -> List["PathReallocation"]:
        astar = BiddingAStar(env)
        res = []
        to_add = set(agents)
        while len(list(to_add)) > 0:
            start_time = time_ns()
            agent = max(to_add, key=lambda _agent: _agent.get_bid(tick).priority)
            to_add.remove(agent)
            bid = agent.get_bid(tick)
            if isinstance(bid, BiddingABBid):
                ab_path, collisions = astar.astar(bid.a, bid.b, agent, bid.flying)
                new_path_segment = PathSegment(bid.a.to_inter_temporal(), bid.b.to_inter_temporal(), 0, ab_path)
                reallocation_reason = AllocationReason(
                    str(Reason.FIRST_ALLOCATION.value)) if agent in agents else AllocationReason(
                    str(Reason.AGENT.value),
                    [collision.id for collision in collisions])
                to_add = to_add.union(collisions)
                for agent_to_remove in collisions:
                    print(f"reallocating: {agent_to_remove.id}")
                    env.deallocate_agent(agent_to_remove, tick)
                    res = [reallocation for reallocation in res if
                           reallocation.agent != agent_to_remove]
                env.allocate_path_segment_for_agent(agent, new_path_segment)
                if agent.id not in env.get_agents():
                    env.add_agent(agent)
                res.append(PathReallocation(agent,
                                            [new_path_segment],
                                            reallocation_reason,
                                            (time_ns() - start_time) / 1e6)
                           )

            if isinstance(bid, BiddingStationaryBid) and isinstance(agent, BiddingStationaryAgent):
                space_segments = []
                blocking_agents = set()
                for block in bid.blocks:
                    intersecting_agents = env.intersect_box(block[0], block[1], False)
                    blocking_agents_block = set()
                    allocateable = True
                    for agent_id in intersecting_agents:
                        if agent_id == agent.id:
                            continue
                        colliding_agent = env.get_agent(agent_id)
                        if colliding_agent.priority < agent.priority:
                            blocking_agents_block.add(colliding_agent)
                        else:
                            allocateable = False
                            break
                    if allocateable:
                        blocking_agents = blocking_agents.union(blocking_agents_block)
                        space_segments.append(SpaceSegment(block[0], block[1]))
                        to_add = to_add.union(blocking_agents_block)
                        for agent_to_remove in blocking_agents_block:
                            print(f"reallocating: {agent_to_remove.id}")
                            env.deallocate_agent(agent_to_remove, tick)
                            res = [reallocation for reallocation in res if
                                   reallocation.agent != agent_to_remove]

                    reallocation_reason = AllocationReason(
                        str(Reason.FIRST_ALLOCATION.value)) if agent in agents else AllocationReason(
                        str(Reason.AGENT.value),
                        [collision.id for collision in blocking_agents])
                    env.allocate_spaces_for_agent(agent, space_segments)
                    if agent.id not in env.get_agents():
                        env.add_agent(agent)
                    res.append(SpaceReallocation(agent,
                                                 space_segments,
                                                 reallocation_reason,
                                                 (time_ns() - start_time) / 1e6)
                               )

        return res
