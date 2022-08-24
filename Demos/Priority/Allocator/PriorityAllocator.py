from time import time_ns

from Simulator import Allocator, PathSegment, AllocationReason, PathAllocation, SpaceSegment, SpaceAllocation, AgentType
from ..AStar.PriorityAStar import PriorityAStar
from ..Owners.PriorityPathOwner import PriorityPathOwner
from ..Owners.PrioritySpaceOwner import PrioritySpaceOwner


class PriorityAllocator(Allocator):
    @staticmethod
    def compatible_owner():
        return [PriorityPathOwner, PrioritySpaceOwner]

    @staticmethod
    def allocate_path(agent, bid, astar):
        a = bid.locations[0]
        time = 0
        count = 0
        optimal_path_segments = []
        collisions = set()
        for b, stay in zip(bid.locations[1:], bid.stays):
            ab_path, intersections = astar.astar(
                a,
                b,
                agent,
            )

            if len(ab_path) == 0:
                return None, set()

            time += ab_path[-1].t - ab_path[0].t
            if time > agent.battery:
                return None, set()

            optimal_path_segments.append(
                PathSegment(a.to_inter_temporal(), b.to_inter_temporal(), count, ab_path))
            collisions = collisions.union(intersections)
            count += 1
            a = ab_path[-1].clone()

        return optimal_path_segments, collisions

    @staticmethod
    def allocate_space(agent, bid, environment):
        optimal_path_segments = []
        collisions = set()
        for block in bid.blocks:
            intersecting_agents = environment.other_agents_in_space(block[0], block[1], agent)
            intersections = [intersecting_agent for intersecting_agent in intersecting_agents if
                             intersecting_agent.priority < agent.priority]
            if len(intersections) == len(intersecting_agents):
                optimal_path_segments.append(SpaceSegment(block[0], block[1]))
                collisions = collisions.union(intersections)
        return optimal_path_segments, collisions

    def allocate_for_agents(self, agents, environment, tick):
        astar = PriorityAStar(environment)
        allocations = []
        to_add = set(agents)
        while len(list(to_add)) > 0:
            start_time = time_ns()
            agent = max(to_add, key=lambda _agent: _agent.get_bid(tick).priority)
            to_add.remove(agent)
            bid = agent.get_bid(tick)

            # Path Agents
            if agent.agent_type == AgentType.PATH.value:
                optimal_path_segments, collisions = self.allocate_path(agent, bid, astar)

                if optimal_path_segments is None:
                    allocations.append(
                        PathAllocation(agent, [], str(AllocationReason.ALLOCATION_FAILED.value),
                                       compute_time=time_ns() - start_time))
                    continue

                # Deallocate collisions
                to_add = to_add.union(collisions)
                for agent_to_remove in collisions:
                    print(f"reallocating: {agent_to_remove.id}")
                    environment.deallocate_agent(agent_to_remove, tick)

                # Allocate Agent
                environment.allocate_path_for_agent(agent, optimal_path_segments)
                allocation_reason = str(AllocationReason.FIRST_ALLOCATION.value) if agent in agents else str(
                    AllocationReason.AGENT.value)
                collision_ids = [collision.id for collision in collisions]
                allocations.append(PathAllocation(agent,
                                                  optimal_path_segments,
                                                  allocation_reason,
                                                  compute_time=time_ns() - start_time,
                                                  colliding_agents_ids=collision_ids))

            # Space Agents
            elif agent.agent_type == AgentType.SPACE.value:
                optimal_space_segments, collisions = self.allocate_space(agent, bid, environment)

                # Deallocate collisions
                to_add = to_add.union(collisions)
                for agent_to_remove in collisions:
                    print(f"reallocating: {agent_to_remove.id}")
                    environment.deallocate_agent(agent_to_remove, tick)

                # Allocate Agent
                environment.allocate_space_for_agent(agent, optimal_space_segments)
                allocation_reason = str(AllocationReason.FIRST_ALLOCATION.value) if agent in agents else str(
                    AllocationReason.AGENT.value)
                collision_ids = [collision.id for collision in collisions]
                allocations.append(SpaceAllocation(agent,
                                                   optimal_space_segments,
                                                   allocation_reason,
                                                   compute_time=time_ns() - start_time,
                                                   colliding_agents_ids=collision_ids))

            if hash(agent) not in environment.agents:
                environment.add_agent(agent)
        return allocations
