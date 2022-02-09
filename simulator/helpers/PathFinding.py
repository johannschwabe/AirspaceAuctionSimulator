from typing import List

from simulator.agents import Agent
from simulator.coordinates.Coordinates import Coordinates
from simulator.coordinates.TimeCoordinates import TimeCoordinates
from simulator.environments.Environment import Environment


# Implemented based on https://www.annytab.com/a-star-search-algorithm-in-python/
def astar(start: TimeCoordinates,
          end: TimeCoordinates,
          agent: Agent,
          env: Environment,
          assume_coords_free: List[TimeCoordinates],
          assume_coords_blocked: List[TimeCoordinates],
          ignore_collisions=False,

          speed=1):
    open_nodes = []
    closed_nodes = []

    start_node = Node(start, None)
    end = Node(end, None)

    open_nodes.append(start_node)
    steps = 0
    while len(open_nodes) > 0 and steps < 200:
        steps += 1
        open_nodes.sort()
        current_node = open_nodes.pop(0)
        closed_nodes.append(current_node)
        if current_node.position == end.position or (current_node.position.t >= end.position.t and current_node.position.inter_temporal_equal(end.position)):
            path = []
            while not current_node.position.inter_temporal_equal(start):
                path.append(current_node.position)
                current_node = current_node.parent
            path.append(current_node.position)
            return path[::-1]

        neighbors = current_node.adjacent_coordinates(speed, env.dimension)
        for next_neighbour in neighbors:
            if env.is_blocked(next_neighbour):
                continue
            field = env.get_field_at(next_neighbour, False)
            if ignore_collisions or next_neighbour in assume_coords_free or ((field.allocated_to is None or field.allocated_to == agent) and next_neighbour not in assume_coords_blocked):
                neighbor = Node(next_neighbour, current_node)
                if neighbor in closed_nodes:
                    continue

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
    print("Astar failed")


def distance(start: TimeCoordinates, end: TimeCoordinates):
    return abs(start.x - end.x) + abs(start.y - end.y) + abs(start.z - end.z) + abs(start.t - end.t)


class Node:
    def __init__(self, position: TimeCoordinates, parent):
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

    def adjacent_coordinates(self, speed: int, dim: Coordinates) -> List[TimeCoordinates]:
        res = [TimeCoordinates(self.position.x, self.position.y, self.position.z, self.position.t + speed)]
        if self.position.x > 0:
            res.append(TimeCoordinates(self.position.x - 1, self.position.y, self.position.z, self.position.t + speed))
        if self.position.y > 0:
            res.append(TimeCoordinates(self.position.x, self.position.y - 1, self.position.z, self.position.t + speed))
        if self.position.z > 0:
            res.append(TimeCoordinates(self.position.x, self.position.y, self.position.z - 1, self.position.t + speed))
        if self.position.x < dim.x - 1:
            res.append(TimeCoordinates(self.position.x + 1, self.position.y, self.position.z, self.position.t + speed))
        if self.position.y < dim.y - 1:
            res.append(TimeCoordinates(self.position.x, self.position.y + 1, self.position.z, self.position.t + speed))
        if self.position.z < dim.z - 1:
            res.append(TimeCoordinates(self.position.x, self.position.y, self.position.z + 1, self.position.t + speed))
        return res
