from time import time_ns

from Mechanisms.Priority.AStar.PriorityAStar import PriorityAStar
from Mechanisms.Priority.BidTracker.PriorityBidTracker import PriorityBidTracker
from Mechanisms.Priority.Bids.PriorityPathBid import PriorityPathBid
from Mechanisms.Priority.Bids.PrioritySpaceBid import PrioritySpaceBid
from Mechanisms.Priority.Owners.PriorityPathOwner import PriorityPathOwner
from Mechanisms.Priority.Owners.PrioritySpaceOwner import PrioritySpaceOwner
from Simulator import Allocator, PathSegment, AllocationReason, SpaceSegment, Allocation
from Simulator.Agents.PathAgent import PathAgent
from Simulator.Agents.SpaceAgent import SpaceAgent
from Simulator.Allocations.AllocationStatistics import AllocationStatistics
from Simulator.BidTracker.BidTracker import BidTracker


class PriorityAllocator(Allocator):
    def __init__(self):
        super().__init__()
        self.bid_tracker = PriorityBidTracker()

    @staticmethod
    def compatible_owner():
        return [PriorityPathOwner, PrioritySpaceOwner]

    @staticmethod
    def allocate_path(agent, bid: PriorityPathBid, astar):
        a = bid.locations[0]
        time = 0
        count = 0
        optimal_path_segments = []
        collisions = set()
        for b, stay in zip(bid.locations[1:], bid.stays):
            ab_path, intersections = astar.astar(
                a,
                b,
                agent,
                bid.flying
            )

            if len(ab_path) == 0:
                return [], set()

            time += ab_path[-1].t - ab_path[0].t
            if time > agent.battery:
                return [], set()

            optimal_path_segments.append(
                PathSegment(a.to_inter_temporal(), b.to_inter_temporal(), count, ab_path))
            collisions = collisions.union(intersections)
            count += 1
            a = ab_path[-1].clone()

        return optimal_path_segments, collisions

    def allocate_space(self, agent, bid: PrioritySpaceBid, environment, tick):
        optimal_path_segments = []
        collisions = set()
        for block in bid.agent.blocks:
            if block[0].t <= tick:
                continue
            intersecting_agents = environment.other_agents_in_space(block[0], block[1], agent)
            intersections = [intersecting_agent for intersecting_agent in intersecting_agents if
                             self.bid_tracker.get_last_bid_for_tick(tick, intersecting_agent,
                                                                    environment).priority < bid.priority]
            if len(intersections) == len(intersecting_agents):
                optimal_path_segments.append(SpaceSegment(block[0], block[1]))
                collisions = collisions.union(intersections)
        return optimal_path_segments, collisions

    def allocate(self, agents, environment, tick):
        astar = PriorityAStar(environment, self.bid_tracker, tick)
        allocations = []
        agents_to_allocate = set(agents)
        while len(list(agents_to_allocate)) > 0:
            start_time = time_ns()
            agent = max(agents_to_allocate,
                        key=lambda _agent: self.bid_tracker.get_last_bid_for_tick(tick, _agent, environment).priority)
            agents_to_allocate.remove(agent)
            bid = self.bid_tracker.get_last_bid_for_tick(tick, agent, environment)

            # Path Agents
            if isinstance(agent, PathAgent):
                optimal_segments, collisions = self.allocate_path(agent, bid, astar)

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

    def get_bid_tracker(self) -> BidTracker:
        return self.bid_tracker
