# Implemented based on https://www.annytab.com/a-star-search-algorithm-in-python/
from Environment import Environment
from coords import Coords
from typing import List

def astar(env: Environment, start: Coords, end: Coords, agent, ignore_reservations=False, speed=1,)->List[Coords]:
    open = []
    closed = []

    start_node = Node(start, None)
    end = Node(end, None)

    open.append(start_node)
    steps = 0
    while len(open) > 0 and steps < 200:
        steps+=1
        open.sort()
        current_node = open.pop(0)
        closed.append(current_node)
        if current_node.posi.intertemporal_equal(end.posi):
            path = []
            while current_node.parent is not None:
                path.append(current_node.posi)
                current_node = current_node.parent
            return path[::-1]

        neighbors = current_node.posi.adjacent(1)
        for next in neighbors:
            field = env.get_field(next, False)
            if not field or (
                    ((field.reserved_for is None or field.reserved_for == agent) or ignore_reservations) and
                     not field.blocked):
                neighbor = Node(next, current_node)
                if neighbor in closed:
                    continue

                neighbor.g = current_node.g + 1
                neighbor.h = distance(neighbor.posi, end.posi)
                neighbor.f = neighbor.g + neighbor.h

                if neighbor in open:
                    alternative_index = open.index(neighbor)
                    alternative = open[alternative_index]
                    if alternative.f > neighbor.f:
                        open[alternative_index] = neighbor
                else:
                    open.append(neighbor)



def distance(start: Coords, end: Coords):
    return abs(start.x - end.x) + abs(start.y - end.y) + abs(start.z - end.z)

class Node:
    def __init__(self, position: Coords, parent):
        self.posi = position
        self.parent = parent
        self.g = 0      # Distance to start node
        self.h = 0      # Distance to goal node
        self.f = 0      # Total cost

    def __eq__(self, other):
        return self.posi == other.posi

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"{self.posi}: {self.f}"