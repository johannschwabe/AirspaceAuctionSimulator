from time import time_ns
from typing import List, Optional, Dict, TYPE_CHECKING, Tuple

from Simulator import Allocator, AStar, PathSegment, SpaceSegment, Allocation, AllocationReason, \
    AllocationStatistics, Agent, BidTracker
from Simulator.Coordinates.Coordinate4D import Coordinate4D
from ..BidTracker.FCFSBidTracker import FCFSBidTracker
from ..BiddingStrategy.FCFSPathBiddingStrategy import FCFSPathBiddingStrategy
from ..BiddingStrategy.FCFSSpaceBiddingStrategy import FCFSSpaceBiddingStrategy
from ..Bids.FCFSPathBid import FCFSPathBid
from ..Bids.FCFSSpaceBid import FCFSSpaceBid
from ..PaymentRule.FCFSPaymentRule import FCFSPaymentRule

if TYPE_CHECKING:
    from Simulator import Environment


class FCFSAllocator(Allocator):
    """
    Allocates agents in the order they arrive.
    There is no given order for agents arriving during same tick.
    """

    @staticmethod
    def compatible_payment_functions():
        return [FCFSPaymentRule]

    def __init__(self):
        """
        Initialize the FCFS-bid-tracker.
        """
        self.bid_tracker = FCFSBidTracker()

    @staticmethod
    def compatible_bidding_strategies():
        """
        Compatible owners are FCFS-[space|path]-owner.
        :return:
        """
        return [FCFSSpaceBiddingStrategy, FCFSPathBiddingStrategy]

    @staticmethod
    def find_valid_tick(position: "Coordinate4D", astar: "AStar", bid: "FCFSPathBid", min_tick: int, max_tick: int):
        if position.t < min_tick:
            position.t = min_tick
        while True:
            valid, _ = astar.is_valid_for_allocation(position, bid.agent)
            if valid:
                break
            position.t += 1
            if position.t > max_tick:
                return None
        return position

    @staticmethod
    def allocate_path(bid: "FCFSPathBid", environment: "Environment", astar: "AStar",
                      tick: int) -> Tuple[Optional[List["PathSegment"]], str]:
        """
        AAllocate a path for a given path-bid.
        Returns `None` if no valid path could be allocated.
        :param bid:
        :param environment:
        :param astar:
        :param tick:
        :return:
        """
        a = bid.locations[0]
        start = a.to_3D()
        a = a.clone()

        time = 0
        count = 0
        optimal_path_segments = []

        for b, stay in zip(bid.locations[1:], bid.stays):

            end = b.to_3D()
            b = b.clone()

            if environment.is_blocked_forever(a, bid.agent.near_radius):
                return None, f"Static blocker at start {a}."

            if environment.is_blocked_forever(b, bid.agent.near_radius):
                return None, f"Static blocker at target {b}."

            a = FCFSAllocator.find_valid_tick(a, astar, bid, tick, environment.dimension.t)
            if a is None:
                return None, f"Start {a} is invalid until max tick {environment.dimension.t}."

            b = FCFSAllocator.find_valid_tick(b, astar, bid, a.t, environment.dimension.t)
            if b is None:
                return None, f"Target {b} is invalid until max tick {environment.dimension.t}."

            ab_path, _ = astar.astar(
                a,
                b,
                bid.agent,
            )

            if len(ab_path) == 0:
                return None, f"No path {a} -> {b} found."

            time += ab_path[-1].t - ab_path[0].t
            if time > bid.battery:
                return None, f"Not enough battery left for path {a} -> {b}."

            optimal_path_segments.append(
                PathSegment(start, end, count, ab_path))

            count += 1

            a = ab_path[-1]
            start = a.to_3D()
            a = a.clone()
            a.t += stay

        return optimal_path_segments, "Path allocated."

    @staticmethod
    def allocate_space(bid: "FCFSSpaceBid", environment: "Environment", tick: int) -> List["SpaceSegment"]:
        """
        Allocate spaces for a given space-bid.
        Returns `[]` if no valid spaces could be allocated.
        :param bid:
        :param environment:
        :param tick:
        :return:
        """
        optimal_path_segments = []
        for block in bid.blocks:
            lower = block[0].clone()
            upper = block[1].clone()

            invalid_block = False
            while lower.t <= tick:
                lower.t += 1
                if lower.t > environment.dimension.t or lower.t > upper.t:
                    print(f"Lower {lower} is invalid until tick {min(environment.dimension.t, upper.t)}.")
                    invalid_block = True
                    break

            if invalid_block:
                continue

            intersecting_agents = environment.other_agents_in_space(lower, upper, bid.agent)
            if len(intersecting_agents) == 0:
                optimal_path_segments.append(SpaceSegment(lower, upper))
        return optimal_path_segments

    def get_bid_tracker(self) -> BidTracker:
        return self.bid_tracker

    def allocate(self, agents: List["Agent"], environment: "Environment", tick: int) -> Dict["Agent", "Allocation"]:
        astar = AStar(environment, self.bid_tracker, tick)
        allocations: Dict["Agent", "Allocation"] = {}

        for agent in agents:
            start_time = time_ns()
            bid = self.bid_tracker.request_new_bid(tick, agent, environment)

            if bid is None:
                allocations[agent] = Allocation(agent, [],
                                                AllocationStatistics(time_ns() - start_time,
                                                                     AllocationReason.ALLOCATION_FAILED,
                                                                     "Crashed."))
                continue

            # Path Agents
            if isinstance(bid, FCFSPathBid):
                optimal_segments, reason = self.allocate_path(bid, environment, astar, tick)

                if optimal_segments is None:
                    allocations[agent] = Allocation(agent, [],
                                                    AllocationStatistics(time_ns() - start_time,
                                                                         AllocationReason.ALLOCATION_FAILED,
                                                                         reason))
                    continue

            # Space Agents
            elif isinstance(bid, FCFSSpaceBid):
                optimal_segments = self.allocate_space(bid, environment, tick)
                reason = "Space allocated."

            else:
                raise Exception(f"Invalid Bid: {bid}")

            new_allocation = Allocation(agent, optimal_segments,
                                        AllocationStatistics(time_ns() - start_time,
                                                             AllocationReason.FIRST_ALLOCATION,
                                                             reason))
            allocations[agent] = new_allocation
            environment.allocate_segments_for_agents([new_allocation], tick)

        return allocations

    def get_bid_tracker(self) -> "FCFSBidTracker":
        """
        Returns the active bid-tracker.
        :return:
        """
        return self.bid_tracker
