from typing import List

from simulator.agents import Agent
from simulator.allocators.Allocator import Allocator
from simulator.coordinates.Coordinates import Coordinates
from simulator.coordinates.TimeCoordinates import TimeCoordinates


# Implemented based on https://www.annytab.com/a-star-search-algorithm-in-python/
def astar(start: TimeCoordinates, end: TimeCoordinates, agent: Agent, allocator: Allocator, speed=1):
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
        if current_node.position.inter_temporal_equal(end.position):
            path = []
            while not current_node.position.inter_temporal_equal(start):
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        neighbors = current_node.adjacent_coordinates(speed)
        for next_neighbour in neighbors:
            field = allocator.get_field_at(next_neighbour)
            if field.is_free_for_agent(agent):
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


def distance(start: Coordinates, end: Coordinates):
    return abs(start.x - end.x) + abs(start.y - end.y) + abs(start.z - end.z)


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

    def adjacent_coordinates(self, speed) -> List[TimeCoordinates]:
        pass
