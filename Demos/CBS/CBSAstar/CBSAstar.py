import heapq
from typing import List, TYPE_CHECKING, Optional, Set

from Simulator.AStar.Node import Node
from Simulator.Agents.PathAgent import PathAgent

if TYPE_CHECKING:
    from Simulator.Coordinates.Coordinate4D import Coordinate4D
    from Simulator.Environment.Environment import Environment


class CBSAStar:
    """
    Optimal Astar for CBS. Positions are only valid if they are not in the constraints of the agent
    """

    def __init__(self, environment: "Environment", max_iter: int = 4_000_000):
        self.environment: "Environment" = environment
        self.max_iter: int = max_iter

    # Implementation based on https://www.annytab.com/a-star-search-algorithm-in-python/
    def astar_loop(self,
                   start: "Coordinate4D",
                   end: "Coordinate4D",
                   agent: "PathAgent",
                   constraints: "Set[Coordinate4D]"):
        """
        Computes a path for a single agent respecting the agents constraints
        :param start:
        :param end:
        :param agent:
        :param constraints:
        :return:
        """
        open_nodes = {}
        closed_nodes = {}
        heap = []

        start_node = Node(start, None, set())
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
                path = reverse_path[::-1]
                break

            # Find non-occupied neighbor
            neighbors = current_node.adjacent_coordinates(self.environment.dimension, agent.speed)
            for next_neighbor in neighbors:
                valid = is_valid_for_path_allocation(self.environment, next_neighbor, agent, constraints)
                if valid and next_neighbor.t <= self.environment.dimension.t:
                    neighbor = Node(next_neighbor, current_node, set())

                    # Closed node
                    if hash(neighbor) in closed_nodes:
                        continue

                    neighbor.g = current_node.g + 1
                    neighbor.h = neighbor.position.distance(end_node.position, l2=False)
                    neighbor.f = neighbor.g + neighbor.h

                    if hash(neighbor) in open_nodes:
                        if open_nodes[hash(neighbor)].f > neighbor.f:
                            open_nodes[hash(neighbor)] = neighbor
                    else:
                        open_nodes[hash(neighbor)] = neighbor
                        heapq.heappush(heap, neighbor)
        return path, steps

    @staticmethod
    def complete_path(path: List["Coordinate4D"], agent: "PathAgent") -> List["Coordinate4D"]:
        """
        Adds waiting coordinates to path where the agents speed is greater than one
        :param path:
        :param agent:
        :return:
        """
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
              agent: "PathAgent",
              constraints: Set["Coordinate4D"]) -> List["Coordinate4D"]:
        """
        Asserts paths plausibility and calls astar-loop
        :param start:
        :param end:
        :param agent:
        :param constraints:
        :return:
        """
        distance = start.distance(end)
        time_left = self.environment.dimension.t - start.t

        if distance * agent.speed > time_left:
            print(f"ASTAR failed: Distance {distance} is too great for agent with speed {agent.speed}.")
            return []

        valid = is_valid_for_path_allocation(self.environment, start, agent, constraints)

        if not valid:
            print(f"ASTAR failed: Start {start} is not valid.")
            return []

        path, steps = self.astar_loop(start, end, agent, constraints)

        if len(path) == 0:
            print(f"ASTAR failed: {'MaxIter' if steps == self.max_iter else 'No valid Allocation'}")
            return []

        complete_path = self.complete_path(path, agent)

        return complete_path


def is_valid_for_path_allocation(env: "Environment", position: "Coordinate4D",
                                 path_agent: "PathAgent", constraints: "Set[Coordinate4D]") -> bool:
    """
    Checks if the position is blocked or in the agent's constraints
    :param env:
    :param position:
    :param path_agent:
    :param constraints:
    :return:
    """
    if position in constraints:
        return False
    if env.is_coordinate_blocked(position, path_agent):
        return False
    return True


def find_valid_path_tick(environment: "Environment", position: "Coordinate4D",
                         path_agent: "PathAgent", min_tick: int, max_tick: int,
                         constraints: "Set[Coordinate4D]") -> Optional[int]:
    """
    Finds the first tick where it can allocate a position
    :param environment:
    :param position:
    :param path_agent:
    :param min_tick:
    :param max_tick:
    :param constraints:
    :return:
    """
    pos_clone = position.clone()
    assert isinstance(path_agent, PathAgent)
    if pos_clone.t < min_tick:
        pos_clone.t = min_tick
    while True:
        valid = is_valid_for_path_allocation(environment, pos_clone, path_agent, constraints)
        if valid:
            break
        pos_clone.t += 1
        if pos_clone.t > max_tick:
            return None
    return pos_clone.t
