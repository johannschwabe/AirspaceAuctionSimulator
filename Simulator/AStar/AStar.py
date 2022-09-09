import heapq
import math
from typing import List, TYPE_CHECKING, Set, Tuple

from .Node import Node
from ..Agents.PathAgent import PathAgent

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

    def is_valid_for_allocation(self, position, agent):
        if self.environment.is_blocked(position, agent):
            return False, None

        my_bid = self.bid_tracker.get_last_bid_for_tick(self.tick, agent, self.environment)

        if my_bid is None:
            return False, None

        colliding_agents = set()

        if position.t == self.tick:
            my_pos = agent.get_position_at_tick(self.tick)
            if my_pos is not None and my_pos == position:
                return True, colliding_agents
            return False, None

        colliding_agents = self.environment.intersect_path_coordinate(position, agent)

        for colliding_agent in colliding_agents:
            if isinstance(colliding_agent, PathAgent):
                distance = position.inter_temporal_distance(colliding_agent.get_position_at_tick(position.t))
                if distance > max(agent.near_radius, colliding_agent.near_radius):
                    continue
            other_bid = self.bid_tracker.get_last_bid_for_tick(self.tick, colliding_agent, self.environment)
            if other_bid is None or my_bid > other_bid:
                colliding_agents.add(colliding_agent)
            else:
                return False, None
        return True, colliding_agents

    @staticmethod
    def distance(start: "Coordinate4D", end: "Coordinate4D"):
        return abs(start.x - end.x) + abs(start.y - end.y) + abs(start.z - end.z)

    @staticmethod
    def distance2(start: "Coordinate4D", end: "Coordinate4D"):
        return math.pow((start.x - end.x) ** 2 + (start.y - end.y) ** 2 + (start.z - end.z) ** 2, 0.5)
