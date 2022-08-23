import heapq
import math
from typing import List, TYPE_CHECKING, Set, Optional, Tuple

from .Node import Node

if TYPE_CHECKING:
    from ..Environment.Environment import Environment
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Agents.PathAgents.PathAgent import PathAgent


class AStar:
    def __init__(self,
                 environment: "Environment",
                 max_iter: int = 100_000,
                 g_sum: float = 0.1,
                 height_adjust: bool = True):
        self.environment: "Environment" = environment
        self.max_iter: int = max_iter
        self.g_sum: float = g_sum
        self.height_adjust: bool = height_adjust

    def valid_start(self,
                    start: "Coordinate4D",
                    agent: "PathAgent",
                    in_air: bool) -> tuple[Optional["Coordinate4D"], set["PathAgent"]]:
        valid_start: "Coordinate4D" = start.clone()

        if in_air and not self.is_valid_for_allocation(valid_start, agent):
            print("In air start is not valid")
            return None, set()

        if self.environment.is_blocked_forever(valid_start, agent.near_radius, agent.speed):
            print("Static Blocker at start")
            return None, set()

        valid, collisions = self.is_valid_for_allocation(valid_start, agent)
        while not valid and valid_start.t < self.environment.dimension.t:
            valid_start.t += 1
            valid, collisions = self.is_valid_for_allocation(valid_start, agent)

        if not valid:
            print("No valid start in environment t-dimension found.")
            return None, set()

        return valid_start, collisions

    # Implementation based on https://www.annytab.com/a-star-search-algorithm-in-python/
    def astar_loop(self,
                   start: "Coordinate4D",
                   end: "Coordinate4D",
                   agent: "PathAgent",
                   start_collisions: Set["PathAgent"]):
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

        while len(open_nodes) > 0 and steps < self.max_iter:
            steps += 1

            current_node = heapq.heappop(heap)

            del open_nodes[hash(current_node)]
            closed_nodes[hash(current_node)] = current_node

            # Target reached
            if current_node.position.inter_temporal_equal(end_node.position):
                reverse_path = []
                while not current_node.position.inter_temporal_equal(start_node.position):
                    reverse_path.append(current_node.position)
                    total_collisions = total_collisions.union(current_node.collisions)
                    current_node = current_node.parent

                reverse_path.append(current_node.position)
                total_collisions.union(current_node.collisions)
                path = reverse_path[::-1]
                break

            # Find non-occupied neighbor
            neighbors = current_node.adjacent_coordinates(self.environment.dimension, agent.speed)
            for next_neighbor in neighbors:
                valid, collisions = self.is_valid_for_allocation(next_neighbor, agent)
                if valid and next_neighbor.t <= self.environment.dimension.t:
                    neighbor = Node(next_neighbor, current_node, set())

                    # Closed node
                    if hash(neighbor) in closed_nodes:
                        continue

                    neighbor.g = current_node.g + self.g_sum
                    neighbor.h = self.distance2(neighbor.position, end_node.position)
                    neighbor.f = neighbor.g + neighbor.h

                    if self.height_adjust:
                        neighbor.f -= neighbor.position.y / self.environment.dimension.y * 0.05 * neighbor.h

                    if hash(neighbor) in open_nodes:
                        if open_nodes[hash(neighbor)].f > neighbor.f:
                            open_nodes[hash(neighbor)] = neighbor
                    else:
                        open_nodes[hash(neighbor)] = neighbor
                        heapq.heappush(heap, neighbor)
        return path, steps, total_collisions

    def complete_path(self, path: List["Coordinate4D"], steps: int, agent: "PathAgent"):
        if len(path) == 0:
            print(f"ASTAR failed: {'MaxIter' if steps == self.max_iter else 'No valid Allocation'}")

        wait_coords: List["Coordinate4D"] = []
        for near_coord in path:
            for t in range(1, agent.speed):
                wait_coord = near_coord.clone()
                wait_coord.t += t
                wait_coords.append(wait_coord)

        complete_path = path + wait_coords
        complete_path.sort(key=lambda x: x.t)
        print(f"PathLen: {len(path)}, steps: {steps}")
        return complete_path

    def astar(
        self,
        start: "Coordinate4D",
        end: "Coordinate4D",
        agent: "PathAgent",
        in_air: bool = False,
    ) -> Tuple[List["Coordinate4D"], set["PathAgent"]]:

        distance = start.inter_temporal_distance(end)
        time_left = self.environment.dimension.t - start.t

        if distance > time_left:
            return [], set()

        valid_start, start_collisions = self.valid_start(start, agent, in_air)

        if valid_start is None:
            return [], start_collisions

        path, steps, collisions = self.astar_loop(valid_start, end, agent, start_collisions)

        complete_path = self.complete_path(path, steps, agent)
        return complete_path, collisions

    def is_valid_for_allocation(self, position: "Coordinate4D", agent: "PathAgent"):
        return self.environment.is_valid_for_allocation(position, agent), set()

    @staticmethod
    def distance(start: "Coordinate4D", end: "Coordinate4D"):
        return abs(start.x - end.x) + abs(start.y - end.y) + abs(start.z - end.z)

    @staticmethod
    def distance15(start: "Coordinate4D", end: "Coordinate4D"):
        return math.pow(abs(start.x - end.x) ** 2 + abs(start.y - end.y) ** 2 + abs(start.z - end.z) ** 2, 0.333)

    @staticmethod
    def distance2(start: "Coordinate4D", end: "Coordinate4D"):
        return math.pow((start.x - end.x) ** 2 + (start.y - end.y) ** 2 + (start.z - end.z) ** 2, 0.5)

    @staticmethod
    def distance3(start: "Coordinate4D", end: "Coordinate4D"):
        return math.pow((start.x - end.x) ** 4 + (start.y - end.y) ** 4 + (start.z - end.z) ** 4, 1 / 4)

    def distance12(self, start: "Coordinate4D", end: "Coordinate4D"):
        return (self.distance(start, end) + self.distance2(start, end)) / 2
