from time import time_ns
from typing import List, TYPE_CHECKING, Set

from Demos.Priority.AStar.PriorityAStar import PriorityAStar
from Demos.Priority.Agents.PriorityABAgent import PriorityABAgent
from Demos.Priority.Agents.PriorityStationaryAgent import PriorityStationaryAgent
from Demos.Priority.Bids.PriorityABBid import PriorityABBid
from Demos.Priority.Bids.PriorityStationaryBid import PriorityStationaryBid
from Demos.Priority.Owners.PriorityABOwner import PriorityABOwner
from Demos.Priority.Owners.PriorityStationaryOwner import PriorityStationaryOwner
from Simulator import Allocator, PathSegment, AllocationType, PathAllocation, Agent, SpaceSegment, SpaceAllocation

if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Allocation.Allocation import Allocation


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
        to_add: Set[Agent] = set(agents)
        while len(list(to_add)) > 0:
            start_time = time_ns()
            agent = max(to_add, key=lambda _agent: _agent.get_bid(tick).priority)
            to_add.remove(agent)
            bid = agent.get_bid(tick)
            if isinstance(bid, PriorityABBid) and isinstance(agent, PriorityABAgent):
                ab_path, collisions = astar.astar(bid.a, bid.b, agent, bid.flying)
                new_path_segment = PathSegment(bid.a.to_inter_temporal(), bid.b.to_inter_temporal(), 0, ab_path)
                allocation_reason = str(AllocationType.FIRST_ALLOCATION.value) if agent in agents else str(
                    AllocationType.AGENT.value)

                collision_ids = None if allocation_reason == str(AllocationType.FIRST_ALLOCATION.value) else [
                    collision.id for collision in collisions]
                to_add = to_add.union(collisions)
                for agent_to_remove in collisions:
                    print(f"reallocating: {agent_to_remove.id}")
                    env.deallocate_agent(agent_to_remove, tick)
                    allocations = [reallocation for reallocation in allocations if
                                   reallocation.agent != agent_to_remove]
                env.allocate_path_segment_for_agent(agent, new_path_segment)
                if agent.id not in env.agents:
                    env.add_agent(agent)
                allocations.append(PathAllocation(agent,
                                                  [new_path_segment],
                                                  allocation_reason,
                                                  compute_time=time_ns() - start_time,
                                                  colliding_agents_ids=collision_ids)
                                   )

            if isinstance(bid, PriorityStationaryBid) and isinstance(agent, PriorityStationaryAgent):
                space_segments = []
                blocking_agents = set()
                for block in bid.blocks:
                    intersecting_agents = env.intersect_space(block[0], block[1])
                    blocking_agents_block = set()
                    allocateable = True
                    for agent_id in intersecting_agents:
                        if agent_id == agent.id:
                            continue
                        colliding_agent = env.agents[agent_id]
                        if isinstance(colliding_agent, PriorityABAgent) and colliding_agent.priority < agent.priority:
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

                    allocation_reason = str(AllocationType.FIRST_ALLOCATION.value) if agent in agents else str(
                        AllocationType.AGENT.value)

                    collision_ids = None if allocation_reason == str(AllocationType.FIRST_ALLOCATION.value) else [
                        collision.id for collision in blocking_agents]
                    env.allocate_space_for_agent(agent, space_segments)
                    if agent.id not in env.agents:
                        env.add_agent(agent)
                    allocations.append(SpaceAllocation(agent,
                                                       space_segments,
                                                       allocation_reason,
                                                       compute_time=time_ns() - start_time,
                                                       colliding_agents_ids=collision_ids)
                                       )

        return allocations
