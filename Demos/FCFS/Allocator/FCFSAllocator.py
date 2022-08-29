from time import time_ns

from Demos.FCFS.BidTracker.FCFSBidTracker import FCFSBidTracker
from Demos.FCFS.Owners.FCFSPathOwner import FCFSPathOwner
from Demos.FCFS.Owners.FCFSSpaceOwner import FCFSSpaceOwner
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
from Simulator.Environment.Environment import Environment


class FCFSAllocator(Allocator):
    def __init__(self):
        super().__init__()
        self.bid_tracker = FCFSBidTracker()

    @staticmethod
    def compatible_owner():
        return [FCFSPathOwner, FCFSSpaceOwner]

    @staticmethod
    def allocate_path(agent, environment: "Environment", astar, tick: int):
        a = agent.locations[0]
        start = a.to_inter_temporal()
        a = a.clone()

        time = 0
        count = 0
        optimal_path_segments = []

        for b, stay in zip(agent.locations[1:], agent.stays):
            end = b.to_inter_temporal()
            b = b.clone()

            if environment.is_blocked_forever(a, agent.near_radius):
                print(f"Static blocker at start {a}.")
                return None

            if environment.is_blocked_forever(b, agent.near_radius):
                print(f"Static blocker at target {b}.")
                return None

            valid, _ = astar.is_valid_for_allocation(a, agent)
            while a.t <= tick or not valid:
                a.t += 1
                if a.t > environment.dimension.t:
                    print(f"Start {a} is invalid until max tick {environment.dimension.t}.")
                    return None
                valid, _ = astar.is_valid_for_allocation(a, agent)

            ab_path, _ = astar.astar(
                a,
                b,
                agent,
            )

            if len(ab_path) == 0:
                print(f"No path {a} -> {b} found.")
                return None

            time += ab_path[-1].t - ab_path[0].t
            if time > agent.battery:
                print(f"Not enough battery left for path {a} -> {b}.")
                return None

            optimal_path_segments.append(
                PathSegment(start, end, count, ab_path))

            count += 1

            a = ab_path[-1]
            start = a.to_inter_temporal()
            a = a.clone()
            a.t += stay

        return optimal_path_segments

    @staticmethod
    def allocate_space(agent, environment):
        optimal_path_segments = []
        for block in agent.blocks:
            intersecting_agents = environment.other_agents_in_space(block[0], block[1], agent)
            if len(intersecting_agents) == 0:
                optimal_path_segments.append(SpaceSegment(block[0], block[1]))
        return optimal_path_segments

    def allocate(self, agents, environment, tick):
        astar = AStar(environment, self.bid_tracker, tick)
        allocations = []

        for agent in agents:
            start_time = time_ns()

            # Path Agents
            if isinstance(agent, PathAgent):
                optimal_segments = self.allocate_path(agent, environment, astar, tick)

                if optimal_segments is None:
                    allocations.append(
                        Allocation(agent, [],
                                   AllocationStatistics(time_ns() - start_time,
                                                        str(AllocationReason.ALLOCATION_FAILED.value))))
                    continue

            # Space Agents
            elif isinstance(agent, SpaceAgent):
                optimal_segments = self.allocate_space(agent, environment)

            else:
                raise Exception(f"Invalid Agent: {agent}")

            new_allocation = Allocation(agent, optimal_segments,
                                        AllocationStatistics(time_ns() - start_time,
                                                             str(AllocationReason.FIRST_ALLOCATION.value)))
            allocations.append(new_allocation)
            environment.allocate_segments_for_agents([new_allocation], tick)

        return allocations

    def get_bid_tracker(self) -> FCFSBidTracker:
        return self.bid_tracker
