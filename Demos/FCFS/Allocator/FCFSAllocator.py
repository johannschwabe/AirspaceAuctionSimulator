from time import time_ns
from typing import List

from ..BiddingStrategy.FCFSPathBiddingStrategy import FCFSPathBiddingStrategy
from ..BiddingStrategy.FCFSSpaceBiddingStrategy import FCFSSpaceBiddingStrategy

from ..PaymentRule.FCFSPaymentRule import FCFSPaymentRule

from Simulator.BidTracker.BidTracker import BidTracker
from Simulator import Allocator, AStar, PathSegment, SpaceSegment, Allocation, AllocationReason, Environment, \
    AllocationStatistics, Agent
from ..BidTracker.FCFSBidTracker import FCFSBidTracker
from ..Bids.FCFSPathBid import FCFSPathBid
from ..Bids.FCFSSpaceBid import FCFSSpaceBid



class FCFSAllocator(Allocator):

    @staticmethod
    def compatible_payment_functions():
        return [FCFSPaymentRule]

    def __init__(self):
        super().__init__()
        self.bid_tracker = FCFSBidTracker()

    @staticmethod
    def compatible_bidding_strategies():
        return [FCFSSpaceBiddingStrategy, FCFSPathBiddingStrategy]

    @staticmethod
    def allocate_path(bid: "FCFSPathBid", environment: "Environment", astar: "AStar", tick: int):
        a = bid.locations[0]
        start = a.to_inter_temporal()
        a = a.clone()

        time = 0
        count = 0
        optimal_path_segments = []

        for b, stay in zip(bid.locations[1:], bid.stays):

            end = b.to_inter_temporal()
            b = b.clone()

            if environment.is_blocked_forever(a, bid.agent.near_radius):
                print(f"Static blocker at start {a}.")
                return None

            if environment.is_blocked_forever(b, bid.agent.near_radius):
                print(f"Static blocker at target {b}.")
                return None

            valid, _ = astar.is_valid_for_allocation(a, bid.agent)
            while a.t <= tick or not valid:
                a.t += 1
                if a.t > environment.dimension.t:
                    print(f"Start {a} is invalid until max tick {environment.dimension.t}.")
                    return None
                valid, _ = astar.is_valid_for_allocation(a, bid.agent)

            ab_path, _ = astar.astar(
                a,
                b,
                bid.agent,
            )

            if len(ab_path) == 0:
                print(f"No path {a} -> {b} found.")
                return None

            time += ab_path[-1].t - ab_path[0].t
            if time > bid.battery:
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
    def allocate_space(bid: "FCFSSpaceBid", environment: "Environment", tick: int):
        optimal_path_segments = []
        for block in bid.blocks:
            lower = block[0].clone()
            upper = block[1].clone()

            while lower.t <= tick:
                lower.t += 1
                if lower.t > environment.dimension.t or lower.t > upper.t:
                    print(f"Lower {lower} is invalid until tick {min(environment.dimension.t, upper.t)}.")
                    return None

            intersecting_agents = environment.other_agents_in_space(lower, upper, bid.agent)
            if len(intersecting_agents) == 0:
                optimal_path_segments.append(SpaceSegment(lower, upper))
        return optimal_path_segments

    def get_bid_tracker(self) -> BidTracker | None:
        return None

    def allocate(self, agents: List["Agent"], environment: "Environment", tick: int):
        astar = AStar(environment, self.bid_tracker, tick)
        allocations = []

        for agent in agents:
            start_time = time_ns()
            bid = self.bid_tracker.request_new_bid(tick, agent, environment)

            if bid is None:
                allocations.append(
                    Allocation(agent, [],
                               AllocationStatistics(time_ns() - start_time,
                                                    str(AllocationReason.CRASH.value))))
                continue

            # Path Agents
            if isinstance(bid, FCFSPathBid):
                optimal_segments = self.allocate_path(bid, environment, astar, tick)

                if optimal_segments is None:
                    allocations.append(
                        Allocation(agent, [],
                                   AllocationStatistics(time_ns() - start_time,
                                                        str(AllocationReason.ALLOCATION_FAILED.value))))
                    continue

            # Space Agents
            elif isinstance(bid, FCFSSpaceBid):
                optimal_segments = self.allocate_space(bid, environment, tick)

            else:
                raise Exception(f"Invalid Bid: {bid}")

            new_allocation = Allocation(agent, optimal_segments,
                                        AllocationStatistics(time_ns() - start_time,
                                                             str(AllocationReason.FIRST_ALLOCATION.value)))
            allocations.append(new_allocation)
            environment.allocate_segments_for_agents([new_allocation], tick)

        return allocations

    def get_bid_tracker(self) -> FCFSBidTracker:
        return self.bid_tracker
