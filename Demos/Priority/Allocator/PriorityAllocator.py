from time import time_ns
from typing import Dict, List, Optional, Set, TYPE_CHECKING, Tuple

from API.WebClasses import WebAllocator
from Simulator import AStar, Allocation, AllocationHistory, AllocationReason, PathSegment, SpaceSegment, \
    find_valid_path_tick, find_valid_space_tick, is_valid_for_path_allocation, is_valid_for_space_allocation
from ..BidTracker.PriorityBidTracker import PriorityBidTracker
from ..BiddingStrategy.PriorityPathBiddingStrategy import PriorityPathBiddingStrategy
from ..BiddingStrategy.PrioritySpaceBiddingStrategy import PrioritySpaceBiddingStrategy
from ..Bids.PriorityPathBid import PriorityPathBid
from ..Bids.PrioritySpaceBid import PrioritySpaceBid
from ..PaymentRule.PriorityPaymentRule import PriorityPaymentRule

if TYPE_CHECKING:
    from Simulator import Environment, Agent


class PriorityAllocator(WebAllocator):
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

    def allocate_path(self, bid: "PriorityPathBid", environment: "Environment", astar: "AStar",
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

        if bid.flying:
            if a.t != tick:
                print(f"not next tick{bid.agent} - {tick}")
                return None, None, f"Cannot teleport to {a} at tick {tick}."
            allocated_segments = bid.agent.allocated_segments

            # If an agents already waited at a position for already part of his speed he can start his allocation
            # in the past and thus wait at most his speed
            if len(allocated_segments) > 0 and len(allocated_segments[-1].coordinates) > 0 \
                    and allocated_segments[-1].coordinates[-1].inter_temporal_equal(a) \
                    and allocated_segments[-1].index == bid.index:
                idx = 1
                while len(allocated_segments[-1].coordinates) > idx \
                        and allocated_segments[-1].coordinates[-(idx + 1)].inter_temporal_equal(a) \
                        and idx < bid.agent.speed:
                    idx += 1
                print(f"moved start for agent {bid.agent} from {a} to {allocated_segments[-1].coordinates[-idx].t} ")
                a.t = allocated_segments[-1].coordinates[-idx].t

            valid, _ = is_valid_for_path_allocation(tick, environment, self.bid_tracker, a, bid.agent)
            if not valid:
                print(f"no valid re-start {bid.agent} - {tick} - {a}")
                return None, None, f"Cannot escape {a}."

        elif a.t == tick:
            a.t += 1

        time = 0
        segment_index = bid.index
        optimal_path_segments = []
        total_collisions = set()

        for _index, b in enumerate(bid.locations[1:]):

            end = b.to_3D()
            b = b.clone()

            if environment.is_coordinate_blocked_forever(a, bid.agent.near_radius):
                return None, None, f"Static blocker at start {a}."

            if environment.is_coordinate_blocked_forever(b, bid.agent.near_radius):
                return None, None, f"Static blocker at target {b}."

            a_t = find_valid_path_tick(tick, environment, self.bid_tracker, a, bid.agent, tick - bid.agent.speed,
                                       environment.dimension.t)
            if a_t is None:
                return None, None, f"Start {a} is invalid until max tick {environment.dimension.t}."
            a.t = a_t

            b_t = find_valid_path_tick(tick, environment, self.bid_tracker, b, bid.agent, a.t, environment.dimension.t)
            if b_t is None:
                return None, None, f"Target {b} is invalid until max tick {environment.dimension.t}."
            b.t = b_t

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
                PathSegment(start, end, segment_index, ab_path))
            total_collisions = total_collisions.union(path_collisions)

            segment_index += 1

            a = ab_path[-1]
            start = a.to_3D()
            a = a.clone()
            if len(bid.stays) > _index:
                a.t = max(a.t, b.t) + bid.stays[_index]

        return optimal_path_segments, total_collisions, "Path allocated."

    def allocate_space(self, bid: "PrioritySpaceBid", environment: "Environment",
                       tick: int) -> Tuple[List["SpaceSegment"], Optional[Set["Agent"]], str]:
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
        collisions = set()
        for block in bid.blocks:
            lower = block.min.clone()
            upper = block.max.clone()

            t = find_valid_space_tick(tick, environment, self.bid_tracker, lower, upper, bid.agent, tick,
                                      environment.dimension.t)
            if t is None:
                continue

            lower.t = t

            valid, block_collisions = is_valid_for_space_allocation(tick, environment, self.bid_tracker, lower, upper,
                                                                    bid.agent)
            if valid:
                collisions = collisions.union(block_collisions)
                possible_space_segments.append(SpaceSegment(lower, upper, block.index))

        return possible_space_segments, collisions, "Space allocated."

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
        displacements: Dict["Agent", Set["Agent"]] = {}
        agents_to_allocate = set(agents)
        while len(agents_to_allocate) > 0:
            start_time = time_ns()

            # Enforce consistent ordering of agents by firstly sorting by priority and secondly by hash
            max_prio = max([self.priority(_agent, tick, environment) for _agent in agents_to_allocate])
            agent = max(
                [_agent for _agent in agents_to_allocate if self.priority(_agent, tick, environment) == max_prio],
                key=lambda _agent: hash(_agent))
            agents_to_allocate.remove(agent)
            print(f"allocating: {agent}")
            bid = self.bid_tracker.request_new_bid(tick, agent, environment)

            if bid is None:
                raise Exception(f"Agent is stuck: {agent}")

            # Path Agents
            if isinstance(bid, PriorityPathBid):
                optimal_segments, collisions, explanation = self.allocate_path(bid, environment, astar, tick)

                if optimal_segments is None:
                    allocations[agent] = Allocation(agent, [],
                                                    AllocationHistory(bid,
                                                                      time_ns() - start_time,
                                                                      AllocationReason.ALLOCATION_FAILED,
                                                                      explanation))
                    continue

            # Space Agents
            elif isinstance(bid, PrioritySpaceBid):
                optimal_segments, collisions, explanation = self.allocate_space(bid, environment, tick)

            else:
                raise Exception(f"Invalid Bid: {bid}")

            # Deallocate collisions
            agents_to_allocate = agents_to_allocate.union(collisions)
            for agent_to_remove in collisions:
                print(f"reallocating: {agent_to_remove}")
                if agent_to_remove not in displacements:
                    displacements[agent_to_remove] = set()
                displacements[agent_to_remove].add(agent)
                environment.deallocate_agent(agent_to_remove, tick)

            # Allocate Agent
            reason = AllocationReason.FIRST_ALLOCATION if agent in agents else AllocationReason.REALLOCATION
            displacing_agent_bids = {}
            if agent in displacements:
                for displacing_agent in displacements[agent]:
                    displacing_agent_bids[displacing_agent.id] = \
                        self.bid_tracker.get_last_bid_for_tick(tick,
                                                               displacing_agent,
                                                               environment)
            colliding_agent_bids = {}
            for colliding_agent in collisions:
                colliding_agent_bids[colliding_agent.id] = \
                    self.bid_tracker.get_last_bid_for_tick(tick,
                                                           colliding_agent,
                                                           environment)

            new_allocation = Allocation(agent,
                                        optimal_segments,
                                        AllocationHistory(bid,
                                                          time_ns() - start_time,
                                                          reason,
                                                          explanation,
                                                          colliding_agent_bids=colliding_agent_bids,
                                                          displacing_agent_bids=displacing_agent_bids))
            allocations[agent] = new_allocation
            environment.allocate_segments_for_agents([new_allocation], tick)

        return allocations

    def get_bid_tracker(self) -> "PriorityBidTracker":
        """
        Returns the active bid-tracker.
        :return:
        """
        return self.bid_tracker
