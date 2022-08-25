from time import time_ns

from Mechanisms.FCFS.Owners.FCFSPathOwner import FCFSPathOwner
from Mechanisms.FCFS.Owners.FCFSSpaceOwner import FCFSSpaceOwner
from Simulator import \
    Allocator, \
    AStar, \
    PathSegment, \
    SpaceSegment, \
    Allocation, \
    AllocationReason, \
    PathAgent, \
    SpaceAgent
from Simulator.Allocations.AllocationStatistics import AllocationStatistics


class FCFSAllocator(Allocator):
    @staticmethod
    def compatible_owner():
        return [FCFSPathOwner, FCFSSpaceOwner]

    @staticmethod
    def allocate_path(agent, astar):
        a = agent.locations[0]
        time = 0
        count = 0
        optimal_path_segments = []
        for b, stay in zip(agent.locations[1:], agent.stays):
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
    def allocate_space(agent, environment):
        optimal_path_segments = []
        for block in agent.blocks:
            intersecting_agents = environment.other_agents_in_space(block[0], block[1], agent)
            if len(intersecting_agents) == 0:
                optimal_path_segments.append(SpaceSegment(block[0], block[1]))
        return optimal_path_segments

    def allocate(self,
                 bids,
                 environment,
                 tick):
        astar = AStar(environment)
        allocations = []
        for bid in bids:
            start_time = time_ns()
            agent = bid.agent

            # Path Agents
            if isinstance(agent, PathAgent):
                optimal_path_segments = self.allocate_path(agent, astar)

                if optimal_path_segments is None:
                    allocations.append(
                        Allocation(agent, [], bid,
                                   AllocationStatistics(time_ns() - start_time,
                                                        str(AllocationReason.ALLOCATION_FAILED.value))))
                    continue

                environment.allocate_path_for_agent(agent, optimal_path_segments)
                allocations.append(
                    Allocation(agent, optimal_path_segments, bid,
                               AllocationStatistics(time_ns() - start_time,
                                                    str(AllocationReason.FIRST_ALLOCATION.value))))

            # Space Agents
            elif isinstance(agent, SpaceAgent):
                optimal_space_segments = self.allocate_space(agent, environment)

                environment.allocate_space_for_agent(agent, optimal_space_segments)
                allocations.append(
                    Allocation(agent, optimal_space_segments, bid,
                               AllocationStatistics(time_ns() - start_time,
                                                    str(AllocationReason.FIRST_ALLOCATION.value))))

            else:
                raise Exception(f"Invalid Agent: {agent}")

            environment.add_agent(agent)
        return allocations
