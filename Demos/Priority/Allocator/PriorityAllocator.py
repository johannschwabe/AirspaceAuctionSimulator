from time import time_ns

from Demos.Priority.AStar.PriorityAStar import PriorityAStar
from Demos.Priority.Agents.PriorityPathAgent import PriorityPathAgent
from Demos.Priority.Agents.PrioritySpaceAgent import PrioritySpaceAgent
from Demos.Priority.Bids.PriorityPathBid import PriorityPathBid
from Demos.Priority.Bids.PrioritySpaceBid import PrioritySpaceBid
from Demos.Priority.Owners.PriorityPathOwner import PriorityPathOwner
from Demos.Priority.Owners.PrioritySpaceOwner import PrioritySpaceOwner
from Simulator import Allocator, PathSegment, AllocationReason, PathAllocation, SpaceSegment, SpaceAllocation


class PriorityAllocator(Allocator):
    @staticmethod
    def compatible_owner():
        return [PriorityPathOwner, PrioritySpaceOwner]

    def __init__(self):
        super().__init__()

    def allocate_for_agents(self, agents, environment, tick):
        astar = PriorityAStar(environment)
        allocations = []
        to_add = set(agents)
        while len(list(to_add)) > 0:
            start_time = time_ns()
            agent = max(to_add, key=lambda _agent: _agent.get_bid(tick).priority)
            to_add.remove(agent)
            bid = agent.get_bid(tick)
            if isinstance(bid, PriorityPathBid) and isinstance(agent, PriorityPathAgent):
                ab_path, collisions = astar.astar(bid.a, bid.b, agent, bid.flying)
                new_path_segment = PathSegment(bid.a.to_inter_temporal(), bid.b.to_inter_temporal(), 0, ab_path)
                allocation_reason = str(AllocationReason.FIRST_ALLOCATION.value) if agent in agents else str(
                    AllocationReason.AGENT.value)

                collision_ids = None if allocation_reason == str(AllocationReason.FIRST_ALLOCATION.value) else [
                    collision.id for collision in collisions]
                to_add = to_add.union(collisions)
                for agent_to_remove in collisions:
                    print(f"reallocating: {agent_to_remove.id}")
                    environment.deallocate_agent(agent_to_remove, tick)
                    allocations = [reallocation for reallocation in allocations if
                                   reallocation.agent != agent_to_remove]
                environment.allocate_path_segment_for_agent(agent, new_path_segment)
                if agent.id not in environment.agents:
                    environment.add_agent(agent)
                allocations.append(PathAllocation(agent,
                                                  [new_path_segment],
                                                  allocation_reason,
                                                  compute_time=time_ns() - start_time,
                                                  colliding_agents_ids=collision_ids)
                                   )

            if isinstance(bid, PrioritySpaceBid) and isinstance(agent, PrioritySpaceAgent):
                space_segments = []
                blocking_agents = set()
                for block in bid.blocks:
                    intersecting_agents = environment.other_agents_in_space(block[0], block[1], agent)
                    blocking_agents_block = set()
                    allocateable = True
                    for colliding_agent in intersecting_agents:
                        if isinstance(colliding_agent, PriorityPathAgent) and colliding_agent.priority < agent.priority:
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
                            environment.deallocate_agent(agent_to_remove, tick)
                            allocations = [reallocation for reallocation in allocations if
                                           reallocation.agent != agent_to_remove]

                    allocation_reason = str(AllocationReason.FIRST_ALLOCATION.value) if agent in agents else str(
                        AllocationReason.AGENT.value)

                    collision_ids = None if allocation_reason == str(AllocationReason.FIRST_ALLOCATION.value) else [
                        collision.id for collision in blocking_agents]
                    environment.allocate_space_for_agent(agent, space_segments)
                    if agent.id not in environment.agents:
                        environment.add_agent(agent)
                    allocations.append(SpaceAllocation(agent,
                                                       space_segments,
                                                       allocation_reason,
                                                       compute_time=time_ns() - start_time,
                                                       colliding_agents_ids=collision_ids)
                                       )

        return allocations
