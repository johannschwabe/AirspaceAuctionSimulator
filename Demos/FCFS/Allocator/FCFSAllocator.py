import random
from time import time_ns
from typing import Dict, List, Optional, TYPE_CHECKING, Tuple

from API.WebClasses import WebAllocator
from Simulator import AStar, Agent, Allocation, AllocationHistory, AllocationReason, PathSegment, \
    SpaceSegment, find_valid_path_tick, find_valid_space_tick, is_valid_for_space_allocation
from ..BidTracker.FCFSBidTracker import FCFSBidTracker
from ..BiddingStrategy.FCFSPathBiddingStrategy import FCFSPathBiddingStrategy
from ..BiddingStrategy.FCFSSpaceBiddingStrategy import FCFSSpaceBiddingStrategy
from ..Bids.FCFSPathBid import FCFSPathBid
from ..Bids.FCFSSpaceBid import FCFSSpaceBid
from ..PaymentRule.FCFSPaymentRule import FCFSPaymentRule

if TYPE_CHECKING:
    from Simulator import Environment


class FCFSAllocator(WebAllocator):
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

    def allocate_path(self, bid: "FCFSPathBid", environment: "Environment", astar: "AStar",
                      tick: int) -> Tuple[Optional[List["PathSegment"]], str]:
        """
        Allocate a path for a given path-bid.
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

        for _index, b in enumerate(bid.locations[1:]):

            end = b.to_3D()
            b = b.clone()

            if environment.is_coordinate_blocked_forever(a, bid.agent.near_radius):
                return None, f"Static blocker at start {a}."

            if environment.is_coordinate_blocked_forever(b, bid.agent.near_radius):
                return None, f"Static blocker at target {b}."

            a_t = find_valid_path_tick(tick, environment, self.bid_tracker, a, bid.agent, tick, environment.dimension.t)
            if a_t is None:
                return None, f"Start {a} is invalid until max tick {environment.dimension.t}."
            a.t = a_t

            b_t = find_valid_path_tick(tick, environment, self.bid_tracker, b, bid.agent, a.t, environment.dimension.t)
            if b_t is None:
                return None, f"Target {b} is invalid until max tick {environment.dimension.t}."
            b.t = b_t

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
            if len(bid.stays) > _index:
                a.t = max(a.t, b.t) + bid.stays[_index]

        return optimal_path_segments, "Path allocated."

    def allocate_space(self, bid: "FCFSSpaceBid", environment: "Environment",
                       tick: int) -> Tuple[List["SpaceSegment"], str]:
        """
        Allocate spaces for a given space-bid.
        Returns the allocated spaces and a list of agents that need to be reallocated,
        because they had a lower priority.
        Returns `[], set()` if no valid spaces could be allocated.
        :param bid:
        :param environment:
        :param tick:
        :return:
        """
        possible_space_segments = []
        for idx, block in enumerate(bid.blocks):
            lower = block.min.clone()
            upper = block.max.clone()

            t = find_valid_space_tick(tick, environment, self.bid_tracker, lower, upper, bid.agent, tick,
                                      environment.dimension.t)
            if t is None:
                continue

            lower.t = t

            valid, _ = is_valid_for_space_allocation(tick, environment, self.bid_tracker, lower, upper, bid.agent)
            if valid:
                possible_space_segments.append(SpaceSegment(lower, upper, idx))

        return possible_space_segments, "Space allocated."

    def allocate(self, agents: List["Agent"], environment: "Environment", tick: int) -> Dict["Agent", "Allocation"]:
        """

        :param agents:
        :param environment:
        :param tick:
        :return:
        """
        astar = AStar(environment, self.bid_tracker, tick)
        allocations: Dict["Agent", "Allocation"] = {}
        random.shuffle(agents)

        for agent in agents:
            print(f"allocating: {agent}")
            start_time = time_ns()
            bid = self.bid_tracker.request_new_bid(tick, agent, environment)

            if bid is None:
                raise Exception(f"Agent is stuck. {agent}")

            # Path Agents
            if isinstance(bid, FCFSPathBid):
                optimal_segments, explanation = self.allocate_path(bid, environment, astar, tick)

                if optimal_segments is None:
                    allocations[agent] = Allocation(agent, [],
                                                    AllocationHistory(bid,
                                                                      time_ns() - start_time,
                                                                      AllocationReason.ALLOCATION_FAILED,
                                                                      explanation))
                    continue

            # Space Agents
            elif isinstance(bid, FCFSSpaceBid):
                optimal_segments, explanation = self.allocate_space(bid, environment, tick)

            else:
                raise Exception(f"Invalid Bid: {bid}")

            new_allocation = Allocation(agent, optimal_segments,
                                        AllocationHistory(bid,
                                                          time_ns() - start_time,
                                                          AllocationReason.FIRST_ALLOCATION,
                                                          explanation))
            allocations[agent] = new_allocation
            environment.allocate_segments_for_agents([new_allocation], tick)

        return allocations

    def get_bid_tracker(self) -> "FCFSBidTracker":
        """
        Returns the active bid-tracker.
        :return:
        """
        return self.bid_tracker
