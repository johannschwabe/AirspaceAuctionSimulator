from time import time_ns

from Demos.Priority.BidTracker.PriorityBidTracker import PriorityBidTracker
from Demos.Priority.Bids.PriorityPathBid import PriorityPathBid
from Demos.Priority.Bids.PrioritySpaceBid import PrioritySpaceBid
from Demos.Priority.Owners.PriorityPathOwner import PriorityPathOwner
from Demos.Priority.Owners.PrioritySpaceOwner import PrioritySpaceOwner
from Simulator import Allocator, PathSegment, AllocationReason, SpaceSegment, Allocation
from Simulator.AStar.AStar import AStar
from Simulator.Agents.PathAgent import PathAgent
from Simulator.Agents.SpaceAgent import SpaceAgent
from Simulator.Allocations.AllocationStatistics import AllocationStatistics
from Simulator.Environment.Environment import Environment


class PriorityAllocator(Allocator):
    def __init__(self):
        super().__init__()
        self.bid_tracker = PriorityBidTracker()

    @staticmethod
    def compatible_owner():
        return [PriorityPathOwner, PrioritySpaceOwner]

    @staticmethod
    def allocate_path(agent, bid: PriorityPathBid, environment: "Environment", astar, tick: int):
        a = bid.locations[0]
        start = a.to_inter_temporal()
        a = a.clone()

        if bid.flying and a.t != tick:
            print(f"Cannot teleport to {a} at tick {tick}.")
            return None, None

        if not bid.flying and a.t == tick:
            a.t += 1

        time = 0
        count = 0
        optimal_path_segments = []
        total_collisions = set()
        for b, stay in zip(bid.locations[1:], bid.stays):

            end = b.to_inter_temporal()
            b = b.clone()

            if environment.is_blocked_forever(a, agent.near_radius):
                print(f"Static blocker at start {a}.")
                return None, None

            if environment.is_blocked_forever(b, agent.near_radius):
                print(f"Static blocker at target {b}.")
                return None, None

            valid, _ = astar.is_valid_for_allocation(a, agent)
            while a.t < tick or not valid:
                a.t += 1
                if a.t > environment.dimension.t or bid.flying:
                    print(f"Start {a} is invalid until max tick {environment.dimension.t}.")
                    return None, None
                valid, _ = astar.is_valid_for_allocation(a, agent)

            ab_path, path_collisions = astar.astar(
                a,
                b,
                agent,
            )

            if len(ab_path) == 0:
                print(f"No path {a} -> {b} found.")
                return None, None

            time += ab_path[-1].t - ab_path[0].t
            if time > agent.battery:
                print(f"Not enough battery left for path {a} -> {b}.")
                return None, None

            optimal_path_segments.append(
                PathSegment(start, end, count, ab_path))
            total_collisions = total_collisions.union(path_collisions)

            count += 1
            a = ab_path[-1].clone()

        return optimal_path_segments, total_collisions

    def allocate_space(self, agent, bid: PrioritySpaceBid, environment, tick):
        optimal_path_segments = []
        collisions = set()
        for block in bid.agent.blocks:
            lower = block[0].clone()
            upper = block[1].clone()

            while lower.t <= tick:
                lower.t += 1
                if lower.t > environment.dimension.t or lower.t > upper.t:
                    print(f"Lower {lower} is invalid until tick {min(environment.dimension.t, upper.t)}.")
                    return None, None

            intersecting_agents = environment.other_agents_in_space(lower, upper, agent)
            intersections = []
            for intersecting_agent in intersecting_agents:
                other_bid = self.bid_tracker.get_last_bid_for_tick(tick, intersecting_agent, environment)
                if other_bid is None or bid > other_bid:
                    intersections.append(intersecting_agent)
            if len(intersections) == len(intersecting_agents):
                optimal_path_segments.append(SpaceSegment(lower, upper))
                collisions = collisions.union(intersections)
        return optimal_path_segments, collisions

    def priority(self, agent, tick, environment):
        bid = self.bid_tracker.get_last_bid_for_tick(tick, agent, environment)
        if bid is None:
            return -1
        return bid.priority

    def allocate(self, agents, environment, tick):
        astar = AStar(environment, self.bid_tracker, tick)
        allocations = []
        agents_to_allocate = set(agents)
        while len(list(agents_to_allocate)) > 0:
            start_time = time_ns()
            agent = max(agents_to_allocate, key=lambda _agent: self.priority(_agent, tick, environment))
            agents_to_allocate.remove(agent)
            bid = self.bid_tracker.request_new_bid(tick, agent, environment)

            if bid is None:
                allocations.append(
                    Allocation(agent, [],
                               AllocationStatistics(time_ns() - start_time,
                                                    str(AllocationReason.CRASH.value))))

            # Path Agents
            if isinstance(agent, PathAgent):
                optimal_segments, collisions = self.allocate_path(agent, bid, environment, astar, tick)

                if optimal_segments is None:
                    allocations.append(
                        Allocation(agent, [],
                                   AllocationStatistics(time_ns() - start_time,
                                                        str(AllocationReason.ALLOCATION_FAILED.value))))
                    continue

            # Space Agents
            elif isinstance(agent, SpaceAgent):
                optimal_segments, collisions = self.allocate_space(agent, bid, environment, tick)

            else:
                raise Exception(f"Invalid Agent: {agent}")

            # Deallocate collisions
            agents_to_allocate = agents_to_allocate.union(collisions)
            for agent_to_remove in collisions:
                print(f"reallocating: {agent_to_remove.id}")
                environment.deallocate_agent(agent_to_remove, tick)

            # Allocate Agent
            allocation_reason = str(AllocationReason.FIRST_ALLOCATION.value) if agent in agents else str(
                AllocationReason.AGENT.value)
            collision_ids = [collision.id for collision in collisions]
            new_allocation = Allocation(agent, optimal_segments,
                                        AllocationStatistics(time_ns() - start_time,
                                                             allocation_reason,
                                                             colliding_agents_ids=collision_ids))
            allocations.append(new_allocation)
            environment.allocate_segments_for_agents([new_allocation], tick)

        return allocations

    def get_bid_tracker(self) -> PriorityBidTracker:
        return self.bid_tracker
