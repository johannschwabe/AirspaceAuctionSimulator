from time import time_ns

from Demos.FCFS.BiddingStrategy.FCFSPathBiddingStrategy import FCFSPathBiddingStrategy
from Demos.FCFS.BiddingStrategy.FCFSSpaceBiddingStrategy import FCFSSpaceBiddingStrategy
from Demos.FCFS.PaymentRule.FCFSPaymentRule import FCFSPaymentRule
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
from Simulator.BidTracker.BidTracker import BidTracker


class FCFSAllocator(Allocator):

    @staticmethod
    def compatible_payment_functions():
        return [FCFSPaymentRule]

    @staticmethod
    def compatible_bidding_strategies():
        return [FCFSSpaceBiddingStrategy, FCFSPathBiddingStrategy]

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

    def get_bid_tracker(self) -> BidTracker | None:
        return None

    def allocate(self, agents, environment, tick):
        astar = AStar(environment, self.get_bid_tracker())
        allocations = []
        for agent in agents:
            start_time = time_ns()
            bid = agent.get_bid(tick, environment)

            # Path Agents
            if isinstance(agent, PathAgent):
                optimal_segments = self.allocate_path(agent, astar)

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
