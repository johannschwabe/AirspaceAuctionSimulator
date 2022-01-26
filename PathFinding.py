from Agent import Agent
from Environment import Environment
from Coords import Coords


# Implemented based on https://www.annytab.com/a-star-search-algorithm-in-python/
def astar(start: Coords, end: Coords, agent: Agent, environment: Environment, speed=1):
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
        if current_node.posi.intertemporal_equal(end.posi):
            path = []
            while not current_node.posi.intertemporal_equal(start):
                path.append(current_node.posi)
                current_node = current_node.parent
            return path[::-1]

        neighbors = current_node.posi.adjacent(speed)
        for next_neighbour in neighbors:
            field = environment.get_field(next_neighbour, False)
            if not field or (
                    (field.reserved_for is None or field.reserved_for == agent) and
                    not field.blocked):
                neighbor = Node(next_neighbour, current_node)
                if neighbor in closed_nodes:
                    continue

                neighbor.g = current_node.g + 1
                neighbor.h = distance(neighbor.posi, end.posi)
                neighbor.f = neighbor.g + neighbor.h

                if neighbor in open_nodes:
                    alternative_index = open_nodes.index(neighbor)
                    alternative = open_nodes[alternative_index]
                    if alternative.f > neighbor.f:
                        open_nodes[alternative_index] = neighbor
                else:
                    open_nodes.append(neighbor)


def distance(start: Coords, end: Coords):
    return abs(start.x - end.x) + abs(start.y - end.y) + abs(start.z - end.z)


class Node:
    def __init__(self, position: Coords, parent):
        self.posi = position
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.posi == other.posi

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"{self.posi}: {self.f}"
