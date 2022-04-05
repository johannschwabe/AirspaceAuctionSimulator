from typing import List, Optional

from ..Agent import Agent
from ..Environment import Environment
from ..Time import Tick
from ..Coordinate import TimeCoordinate, Coordinate


# Implemented based on https://www.annytab.com/a-star-search-algorithm-in-python/
def astar(
    start: TimeCoordinate,
    end: TimeCoordinate,
    env: Environment,
    agent: Agent,
):
    open_nodes = []
    closed_nodes = []

    valid_start = start
    while not env.is_valid_for_allocation(valid_start, agent):
        valid_start.t += 1

    start_node = Node(start, None)
    end = Node(end, None)

    open_nodes.append(start_node)
    steps = 0

    path = []

    while len(open_nodes) > 0 and steps < 1000:
        steps += 1
        open_nodes.sort()
        current_node = open_nodes.pop(0)
        closed_nodes.append(current_node)
        # Target reached
        if current_node.position == end.position or (
            current_node.position.t > end.position.t and current_node.position.inter_temporal_equal(end.position)):
            reverse_path = []
            while not current_node.position.inter_temporal_equal(start):
                reverse_path.append(current_node.position)
                current_node = current_node.parent

            reverse_path.append(current_node.position)
            path = reverse_path[::-1]
            break

        # Find non occupied neighbor
        neighbors = current_node.adjacent_coordinates(env._dimension, agent.speed)
        for next_neighbor in neighbors:
            if env.is_valid_for_allocation(next_neighbor, agent):
                waiting_neighbor = Node(next_neighbor, current_node)
                # Closed node
                if waiting_neighbor in closed_nodes:
                    break

                neighbor = Node(next_neighbor, current_node)

                neighbor.g = current_node.g + 1
                neighbor.h = distance(neighbor.position, end.position)
                neighbor.f = neighbor.g + neighbor.h

                if neighbor in open_nodes:
                    alternative_index = open_nodes.index(neighbor)
                    alternative = open_nodes[alternative_index]
                    if alternative.f > neighbor.f:
                        open_nodes[alternative_index] = neighbor

                else:
                    open_nodes.append(neighbor)
    if len(path) == 0:
        print("ASTAR failed")
    wait_coords: List[TimeCoordinate] = []
    for near_coord in path:
        for t in range(1, agent.speed):
            wait_coords.append(TimeCoordinate(near_coord.x, near_coord.y, near_coord.z, near_coord.t + Tick(t)))

    complete_path = path + wait_coords
    complete_path.sort(key=lambda x: x.t)
    return complete_path


def distance(start: Coordinate, end: Coordinate):
    return abs(start.x - end.x) + abs(start.y - end.y) + abs(start.z - end.z)


class Node:
    def __init__(self, position: TimeCoordinate, parent):
        self.position = position
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"{self.position}: {self.f}"

    def adjacent_coordinates(self, dim: Coordinate, speed: int) -> List[TimeCoordinate]:
        res = [TimeCoordinate(self.position.x, self.position.y, self.position.z, Tick(self.position.t + speed))]
        if self.position.x > 0:
            res.append(TimeCoordinate(self.position.x - 1, self.position.y, self.position.z,
                                      Tick(self.position.t + speed)))
        if self.position.y > 0:
            res.append(TimeCoordinate(self.position.x, self.position.y - 1, self.position.z,
                                      Tick(self.position.t + speed)))
        if self.position.z > 0:
            res.append(TimeCoordinate(self.position.x, self.position.y, self.position.z - 1,
                                      Tick(self.position.t + speed)))
        if self.position.x < dim.x - 1:
            res.append(TimeCoordinate(self.position.x + 1, self.position.y, self.position.z,
                                      Tick(self.position.t + speed)))
        if self.position.y < dim.y - 1:
            res.append(TimeCoordinate(self.position.x, self.position.y + 1, self.position.z,
                                      Tick(self.position.t + speed)))
        if self.position.z < dim.z - 1:
            res.append(TimeCoordinate(self.position.x, self.position.y, self.position.z + 1,
                                      Tick(self.position.t + speed)))
        return res
