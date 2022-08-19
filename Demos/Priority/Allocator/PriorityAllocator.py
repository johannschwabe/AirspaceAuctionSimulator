from time import time_ns
from typing import List, TYPE_CHECKING

from AAS.Allocator import Allocator
from AAS.Path import PathAllocation, PathSegment, SpaceSegment, SpaceAllocation
from AAS.Path.AllocationReason import AllocationReason
from AAS.Path.AllocationReasonType import AllocationReasonType
from Demos.Priority.AStar.PriorityAStar import PriorityAStar
from Demos.Priority.Agents.PriorityABAgent import PriorityABAgent
from Demos.Priority.Agents.PriorityStationaryAgent import PriorityStationaryAgent
from Demos.Priority.Bids.PriorityABBid import PriorityABBid
from Demos.Priority.Bids.PriorityStationaryBid import PriorityStationaryBid
from Demos.Priority.Owners.PriorityABOwner import PriorityABOwner
from Demos.Priority.Owners.PriorityStationaryOwner import PriorityStationaryOwner

if TYPE_CHECKING:
    from AAS import Environment
    from AAS.Path.Allocation import Allocation


class PriorityAllocator(Allocator):
    @staticmethod
    def compatible_owner():
        return [PriorityABOwner, PriorityStationaryOwner]

    def __init__(self):
        super().__init__()

    def allocate_for_agents(self,
                            agents: List["PriorityABAgent"],
                            env: "Environment",
                            tick: int) -> List["Allocation"]:
        astar = PriorityAStar(env)
        allocations: List["Allocation"] = []
        to_add = set(agents)
        while len(list(to_add)) > 0:
            start_time = time_ns()
            agent = max(to_add, key=lambda _agent: _agent.get_bid(tick).priority)
            to_add.remove(agent)
            bid = agent.get_bid(tick)
            if isinstance(bid, PriorityABBid):
                ab_path, collisions = astar.astar(bid.a, bid.b, agent, bid.flying)
                new_path_segment = PathSegment(bid.a.to_inter_temporal(), bid.b.to_inter_temporal(), 0, ab_path)
                reallocation_reason = AllocationReason(
                    str(AllocationReasonType.FIRST_ALLOCATION.value)) if agent in agents else AllocationReason(
                    str(AllocationReasonType.AGENT.value),
                    [collision.id for collision in collisions])
                to_add = to_add.union(collisions)
                for agent_to_remove in collisions:
                    print(f"reallocating: {agent_to_remove.id}")
                    env.deallocate_agent(agent_to_remove, tick)
                    allocations = [reallocation for reallocation in allocations if
                                   reallocation.agent != agent_to_remove]
                env.allocate_path_segment_for_agent(agent, new_path_segment)
                if agent.id not in env.get_agents():
                    env.add_agent(agent)
                allocations.append(PathAllocation(agent,
                                                  [new_path_segment],
                                                  reallocation_reason,
                                                  time_ns() - start_time)
                                   )

            if isinstance(bid, PriorityStationaryBid) and isinstance(agent, PriorityStationaryAgent):
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
                            allocations = [reallocation for reallocation in allocations if
                                           reallocation.agent != agent_to_remove]

                    reallocation_reason = AllocationReason(
                        str(AllocationReasonType.FIRST_ALLOCATION.value)) if agent in agents else AllocationReason(
                        str(AllocationReasonType.AGENT.value),
                        [collision.id for collision in blocking_agents])
                    env.allocate_space_for_agent(agent, space_segments)
                    if agent.id not in env.get_agents():
                        env.add_agent(agent)
                    allocations.append(SpaceAllocation(agent,
                                                       space_segments,
                                                       reallocation_reason,
                                                       time_ns() - start_time)
                                       )

        return allocations
