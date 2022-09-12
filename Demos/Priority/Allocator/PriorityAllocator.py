from time import time_ns
from typing import List, Tuple, Set, Optional, Dict, TYPE_CHECKING

from Simulator import Allocator, PathSegment, AllocationReason, SpaceSegment, Allocation, \
    AllocationStatistics, AStar
from Simulator.Coordinates.Coordinate4D import Coordinate4D
from ..BidTracker.PriorityBidTracker import PriorityBidTracker
from ..BiddingStrategy.PriorityPathBiddingStrategy import PriorityPathBiddingStrategy
from ..BiddingStrategy.PrioritySpaceBiddingStrategy import PrioritySpaceBiddingStrategy
from ..Bids.PriorityPathBid import PriorityPathBid
from ..Bids.PrioritySpaceBid import PrioritySpaceBid
from ..PaymentRule.PriorityPaymentRule import PriorityPaymentRule

if TYPE_CHECKING:
    from Simulator import Environment, Agent


class PriorityAllocator(Allocator):
    """
    Allocates agents based on priority of the bid.
    Agents with higher priority bids can deallocate agents with lower priority bids.
    """

    def __init__(self):
        """
        Initialize the priority-bid-tracker that remembers the max priority of an agents bids.
        """
        self.bid_tracker = PriorityBidTracker()

    @staticmethod
    def compatible_bidding_strategies():
        return [PriorityPathBiddingStrategy, PrioritySpaceBiddingStrategy]

    @staticmethod
    def compatible_payment_functions():
        return [PriorityPaymentRule]

    @staticmethod
    def find_valid_tick(position: "Coordinate4D", astar: "AStar", bid: "PriorityPathBid", min_tick: int, max_tick: int):
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
    def allocate_path(bid: "PriorityPathBid", environment: "Environment", astar: "AStar",
                      tick: int) -> Tuple[Optional[List["PathSegment"]], Optional[Set["Agent"]], str]:
        """
        Allocate a path for a given path-bid.
        Returns the allocated path and a list of agents that need to be reallocated, because they had a lower priority.
        Returns `None, None` if no valid path could be allocated.
        :param bid:
        :param environment:
        :param astar:
        :param tick:
        :return:
        """
        a = bid.locations[0]
        start = a.to_3D()
        a = a.clone()

        if bid.flying and a.t != tick:
            return None, None, f"Cannot teleport to {a} at tick {tick}."

        if not bid.flying and a.t == tick:
            a.t += 1

        valid, _ = astar.is_valid_for_allocation(a, bid.agent)
        if not valid and bid.flying:
            return None, None, f"Cannot escape {a}."

        time = 0
        count = 0
        optimal_path_segments = []
        total_collisions = set()

        for b, stay in zip(bid.locations[1:], bid.stays):

            end = b.to_3D()
            b = b.clone()

            if environment.is_blocked_forever(a, bid.agent.near_radius):
                return None, None, f"Static blocker at start {a}."

            if environment.is_blocked_forever(b, bid.agent.near_radius):
                return None, None, f"Static blocker at target {b}."

            a = PriorityAllocator.find_valid_tick(a, astar, bid, tick, environment.dimension.t)
            if a is None:
                return None, None, f"Start {a} is invalid until max tick {environment.dimension.t}."

            b = PriorityAllocator.find_valid_tick(b, astar, bid, a.t, environment.dimension.t)
            if b is None:
                return None, None, f"Target {b} is invalid until max tick {environment.dimension.t}."

            ab_path, path_collisions = astar.astar(
                a,
                b,
                bid.agent,
            )

            if len(ab_path) == 0:
                return None, None, f"No path {a} -> {b} found."

            time += ab_path[-1].t - ab_path[0].t
            if time > bid.battery:
                return None, None, f"Not enough battery left for path {a} -> {b}."

            optimal_path_segments.append(
                PathSegment(start, end, count, ab_path))
            total_collisions = total_collisions.union(path_collisions)

            count += 1

            a = ab_path[-1]
            start = a.to_3D()
            a = a.clone()
            a.t += stay

        return optimal_path_segments, total_collisions, "Path allocated."

    def allocate_space(self, bid: "PrioritySpaceBid", environment: "Environment",
                       tick: int) -> Tuple[List["SpaceSegment"], Set["Agent"]]:
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
        optimal_path_segments = []
        collisions = set()
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
            intersections = []
            for intersecting_agent in intersecting_agents:
                other_bid = self.bid_tracker.get_last_bid_for_tick(tick, intersecting_agent, environment)
                if other_bid is None or bid > other_bid:
                    intersections.append(intersecting_agent)
            if len(intersections) == len(intersecting_agents):
                optimal_path_segments.append(SpaceSegment(lower, upper))
                collisions = collisions.union(intersections)
        return optimal_path_segments, collisions

    def priority(self, agent: "Agent", tick: int, environment: "Environment") -> float:
        """
        Returns the priority of the given agent in the current tick.
        Returns -1. if the bid is None (agent is stuck/crashed).
        :param agent:
        :param tick:
        :param environment:
        :return:
        """
        bid = self.bid_tracker.get_last_bid_for_tick(tick, agent, environment)
        if bid is None:
            return -1.
        return bid.priority

    def allocate(self, agents: List["Agent"], environment: "Environment", tick: int) -> Dict["Agent", "Allocation"]:
        """

        :param agents:
        :param environment:
        :param tick:
        :return:
        """
        astar = AStar(environment, self.bid_tracker, tick)
        allocations: Dict["Agent", "Allocation"] = {}
        agents_to_allocate = set(agents)
        while len(list(agents_to_allocate)) > 0:
            start_time = time_ns()
            agent = max(agents_to_allocate, key=lambda _agent: self.priority(_agent, tick, environment))
            agents_to_allocate.remove(agent)
            bid = self.bid_tracker.request_new_bid(tick, agent, environment)

            if bid is None:
                allocations[agent] = Allocation(agent, [],
                                                AllocationStatistics(time_ns() - start_time,
                                                                     AllocationReason.ALLOCATION_FAILED,
                                                                     "Crashed."))
                continue

            # Path Agents
            if isinstance(bid, PriorityPathBid):
                optimal_segments, collisions, reason = self.allocate_path(bid, environment, astar, tick)

                if optimal_segments is None:
                    allocations[agent] = Allocation(agent, [],
                                                    AllocationStatistics(time_ns() - start_time,
                                                                         AllocationReason.ALLOCATION_FAILED,
                                                                         reason))
                    continue

            # Space Agents
            elif isinstance(bid, PrioritySpaceBid):
                optimal_segments, collisions = self.allocate_space(bid, environment, tick)
                reason = "Space allocated"

            else:
                raise Exception(f"Invalid Bid: {bid}")

            # Deallocate collisions
            agents_to_allocate = agents_to_allocate.union(collisions)
            for agent_to_remove in collisions:
                print(f"reallocating: {agent_to_remove.id}")
                environment.deallocate_agent(agent_to_remove, tick)

            # Allocate Agent
            allocation_type = AllocationReason.FIRST_ALLOCATION if agent in agents else AllocationReason.REALLOCATION
            collision_ids = [collision.id for collision in collisions]
            new_allocation = Allocation(agent, optimal_segments,
                                        AllocationStatistics(time_ns() - start_time,
                                                             allocation_type,
                                                             reason,
                                                             colliding_agent_ids=collision_ids))
            allocations[agent] = new_allocation
            environment.allocate_segments_for_agents([new_allocation], tick)

        return allocations

    def get_bid_tracker(self) -> "PriorityBidTracker":
        """
        Returns the active bid-tracker.
        :return:
        """
        return self.bid_tracker
