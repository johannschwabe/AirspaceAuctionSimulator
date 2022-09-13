import heapq
import math
from typing import List, TYPE_CHECKING, Set, Tuple

from .Node import Node
from ..Agents.PathAgent import PathAgent
from ..Agents.SpaceAgent import SpaceAgent

if TYPE_CHECKING:
    from ..Environment.Environment import Environment
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Agents.Agent import Agent
    from ..BidTracker.BidTracker import BidTracker


class AStar:
    def __init__(self,
                 environment: "Environment",
                 bid_tracker: "BidTracker",
                 tick: int = -1,
                 max_iter: int = 100_000,
                 g_sum: float = 0.2,
                 height_adjust: float = 0.05):
        self.environment: "Environment" = environment
        self.tick: int = tick
        self.max_iter: int = max_iter
        self.g_sum: float = g_sum
        self.height_adjust: float = height_adjust
        self.bid_tracker: "BidTracker" = bid_tracker

    # Implementation based on https://www.annytab.com/a-star-search-algorithm-in-python/
    def astar_loop(self,
                   start: "Coordinate4D",
                   end: "Coordinate4D",
                   agent: "PathAgent",
                   start_collisions: Set["Agent"]):
        open_nodes = {}
        closed_nodes = {}
        heap = []

        start_node = Node(start, None, start_collisions)
        end_node = Node(end, None, set())
        open_nodes[hash(start_node)] = start_node
        heapq.heappush(heap, start_node)

        steps = 0

        path: List["Coordinate4D"] = []

        total_collisions = set()

        while len(open_nodes) > 0 and (self.max_iter == -1 or steps < self.max_iter):
            steps += 1

            current_node = heapq.heappop(heap)

            del open_nodes[hash(current_node)]
            closed_nodes[hash(current_node)] = current_node

            # Target reached
            if current_node.position.inter_temporal_equal(end_node.position):
                reverse_path = []
                while not current_node.position == start_node.position:
                    reverse_path.append(current_node.position)
                    total_collisions = total_collisions.union(current_node.collisions)
                    current_node = current_node.parent

                reverse_path.append(current_node.position)
                total_collisions = total_collisions.union(current_node.collisions)
                path = reverse_path[::-1]
                break

            # Find non-occupied neighbor
            neighbors = current_node.adjacent_coordinates(self.environment.dimension, agent.speed)
            for next_neighbor in neighbors:
                valid, collisions = self.is_valid_for_allocation(next_neighbor, agent)
                if valid and next_neighbor.t <= self.environment.dimension.t:
                    neighbor = Node(next_neighbor, current_node, collisions)

                    # Closed node
                    if hash(neighbor) in closed_nodes:
                        continue

                    neighbor.g = current_node.g + self.g_sum
                    neighbor.h = self.distance2(neighbor.position, end_node.position)
                    neighbor.f = neighbor.g + neighbor.h

                    if self.height_adjust > 0.:
                        neighbor.f -= neighbor.position.y / self.environment.dimension.y * \
                                      self.height_adjust * neighbor.h

                    if hash(neighbor) in open_nodes:
                        if open_nodes[hash(neighbor)].f > neighbor.f:
                            open_nodes[hash(neighbor)] = neighbor
                    else:
                        open_nodes[hash(neighbor)] = neighbor
                        heapq.heappush(heap, neighbor)
        return path, steps, total_collisions

    @staticmethod
    def complete_path(path: List["Coordinate4D"], agent: "PathAgent"):
        wait_coords: List["Coordinate4D"] = []
        for near_coord in path:
            for t in range(1, agent.speed):
                wait_coord = near_coord.clone()
                wait_coord.t += t
                wait_coords.append(wait_coord)

        complete_path = path + wait_coords
        complete_path.sort(key=lambda x: x.t)
        return complete_path

    def astar(self,
              start: "Coordinate4D",
              end: "Coordinate4D",
              agent: "PathAgent") -> Tuple[List["Coordinate4D"], set["Agent"]]:

        if start.t < self.tick:
            print(f"Too late to allocate start {start} at tick {self.tick}.")
            return [], set()

        distance = start.inter_temporal_distance(end)
        time_left = self.environment.dimension.t - start.t

        if distance * agent.speed > time_left:
            print(f"ASTAR failed: Distance {distance} is too great for agent with speed {agent.speed}.")
            return [], set()

        valid, start_collisions = self.is_valid_for_allocation(start, agent)

        if not valid:
            print(f"ASTAR failed: Start {start} is not valid.")
            return [], set()

        path, steps, collisions = self.astar_loop(start, end, agent, start_collisions)

        if len(path) == 0:
            print(f"ASTAR failed: {'MaxIter' if steps == self.max_iter else 'No valid Allocation'}")
            return [], set()

        complete_path = self.complete_path(path, agent)

        print(f"ASTAR: {complete_path[0]} -> {complete_path[-1]},\tPathLen: {len(path):3d},\tSteps: {steps:3d}")
        return complete_path, collisions

    def is_valid_for_allocation(self, position: "Coordinate4D", agent: "PathAgent"):
        if position.t < self.tick:
            raise Exception(f"Cannot validate position in the past. Position: {position}, Tick: {self.tick}.")

        if self.environment.is_blocked(position, agent):
            return False, None

        my_bid = self.bid_tracker.get_last_bid_for_tick(self.tick, agent, self.environment)

        if my_bid is None:
            return False, None

        colliding_agents = set()

        flying = False
        if position.t == self.tick:
            my_pos = agent.get_position_at_tick(self.tick)
            if my_pos is not None and my_pos == position:
                flying = True
            else:
                return False, None

        max_intersecting_agents = self.environment.intersect_path_coordinate(position, agent)
        for intersecting_agent in max_intersecting_agents:
            if isinstance(intersecting_agent, PathAgent):
                max_near_radius = max(agent.near_radius, intersecting_agent.near_radius)
                path_coordinates = intersecting_agent.get_positions_at_ticks(position.t, speed=agent.speed)
                assert len(path_coordinates) > 0
                true_intersection = False
                for path_coordinate in path_coordinates:
                    distance = position.inter_temporal_distance(path_coordinate, l2=True)
                    if distance <= max_near_radius:
                        true_intersection = True
                        break

                if not true_intersection:
                    continue

                if flying:
                    colliding_agents.add(intersecting_agent)
                    continue

                other_bid = self.bid_tracker.get_last_bid_for_tick(self.tick, intersecting_agent, self.environment)
                if other_bid is None:
                    raise Exception(f"Agent stuck: {intersecting_agent}")
                if my_bid > other_bid:
                    other_pos = intersecting_agent.get_position_at_tick(self.tick)
                    if other_pos is not None:
                        # Make sure intersecting agent can dodge in time
                        distance_to_clear = max(2 * max_near_radius - position.inter_temporal_distance(other_pos) + 1,
                                                1)
                        time_to_clearance = distance_to_clear * intersecting_agent.speed
                        if time_to_clearance >= position.t - self.tick:
                            return False, None
                    colliding_agents.add(intersecting_agent)
                else:
                    return False, None

        intersecting_agents = self.environment.intersect_path_coordinate(position, agent, use_max_radius=False)
        for intersecting_agent in intersecting_agents:
            if isinstance(intersecting_agent, SpaceAgent):
                min_distance = math.inf
                for block in intersecting_agent.blocks:
                    distance = position.distance_block(block)

                    if min_distance > distance:
                        min_distance = distance

                if min_distance > agent.near_radius:
                    continue
                other_bid = self.bid_tracker.get_last_bid_for_tick(self.tick, intersecting_agent, self.environment)
                if other_bid is None or my_bid > other_bid:
                    colliding_agents.add(intersecting_agent)
                else:
                    return False, None

        return True, colliding_agents

    @staticmethod
    def distance(start: "Coordinate4D", end: "Coordinate4D"):
        return abs(start.x - end.x) + abs(start.y - end.y) + abs(start.z - end.z)

    @staticmethod
    def distance2(start: "Coordinate4D", end: "Coordinate4D"):
        return math.pow((start.x - end.x) ** 2 + (start.y - end.y) ** 2 + (start.z - end.z) ** 2, 0.5)
