from time import time_ns

from Simulator import \
    Allocator, \
    AStar, \
    AgentType, \
    PathSegment, \
    SpaceSegment, \
    PathAllocation, \
    SpaceAllocation, \
    AllocationReason
from ..Owners.FCFSPathOwner import FCFSPathOwner
from ..Owners.FCFSSpaceOwner import FCFSSpaceOwner


class FCFSAllocator(Allocator):
    @staticmethod
    def compatible_owner():
        return [FCFSPathOwner, FCFSSpaceOwner]

    @staticmethod
    def allocate_path(agent, bid, astar):
        a = bid.locations[0]
        time = 0
        count = 0
        optimal_path_segments = []
        for b, stay in zip(bid.locations[1:], bid.stays):
            ab_path, _ = astar.astar(
                a,
                b,
                agent,
            )

            if len(ab_path) == 0:
                return None

            time += ab_path[-1].t - ab_path[0].t
            if time > agent.battery:
                return None

            optimal_path_segments.append(
                PathSegment(a.to_inter_temporal(), b.to_inter_temporal(), count, ab_path))
            count += 1
            a = ab_path[-1].clone()

        return optimal_path_segments

    @staticmethod
    def allocate_space(agent, bid, environment):
        optimal_path_segments = []
        for block in bid.blocks:
            intersecting_agents = environment.other_agents_in_space(block[0], block[1], agent)
            if len(intersecting_agents) == 0:
                optimal_path_segments.append(SpaceSegment(block[0], block[1]))
        return optimal_path_segments

    def allocate_for_agents(self,
                            agents,
                            environment,
                            tick):
        astar = AStar(environment)
        allocations = []
        for agent in agents:
            start_time = time_ns()
            bid = agent.get_bid(tick)

            # Path Agents
            if agent.agent_type == AgentType.PATH.value:
                optimal_path_segments = self.allocate_path(agent, bid, astar)

                if optimal_path_segments is None:
                    allocations.append(
                        PathAllocation(agent, [], str(AllocationReason.ALLOCATION_FAILED.value),
                                       compute_time=time_ns() - start_time))
                    continue

                environment.allocate_path_for_agent(agent, optimal_path_segments)
                allocations.append(PathAllocation(agent,
                                                  optimal_path_segments,
                                                  str(AllocationReason.FIRST_ALLOCATION.value),
                                                  compute_time=time_ns() - start_time))

            # Space Agents
            elif agent.agent_type == AgentType.SPACE.value:
                optimal_path_segments = self.allocate_space(agent, bid, environment)

                environment.allocate_space_for_agent(agent, optimal_path_segments)
                allocations.append(SpaceAllocation(agent,
                                                   optimal_path_segments,
                                                   str(AllocationReason.FIRST_ALLOCATION.value),
                                                   compute_time=time_ns() - start_time))

            environment.add_agent(agent)
        return allocations
