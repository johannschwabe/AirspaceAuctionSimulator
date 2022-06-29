import math
from typing import List
from time import time_ns

from ..Agent import Agent, PathAgent
from ..Environment import Environment
from ..Time import Tick
from ..Coordinate import TimeCoordinate, Coordinate


# Implemented based on https://www.annytab.com/a-star-search-algorithm-in-python/
def astar(
    start: TimeCoordinate,
    end: TimeCoordinate,
    env: Environment,
    agent: PathAgent,
):
    # print(f"{start} -> {end} ---->", end="")
    # print(f"---->", end="")
    start_time = time_ns()
    open_nodes = {}
    closed_nodes = {}

    valid_start = start
    while not env.is_valid_for_allocation(valid_start, agent):
        valid_start.t += 1

    start_node = Node(start, None)
    end_node = Node(end, None)
    open_nodes[hash(start_node)] = start_node
    steps = 0

    path = []
    sort_time = 0
    neighbors_time = 0
    valid_time = 0
    in_check_t = 0
    in_check_2_t = 0
    MAX_ITER = 10000

    while len(open_nodes) > 0 and steps < MAX_ITER:
        steps += 1

        start_sort = time_ns()
        current_node = min(list(open_nodes.values()))
        sort_time += time_ns() - start_sort

        del open_nodes[hash(current_node)]
        closed_nodes[hash(current_node)] = current_node

        # if steps % 50 == 0:
        #     print(current_node)
        # Target reached
        if current_node.position.inter_temporal_equal(end_node.position):
            reverse_path = []
            while not current_node.position.inter_temporal_equal(start):
                reverse_path.append(current_node.position)
                current_node = current_node.parent

            reverse_path.append(current_node.position)
            path = reverse_path[::-1]
            break

        start_neighbors = time_ns()
        # Find non-occupied neighbor
        neighbors = current_node.adjacent_coordinates(env._dimension, agent.speed)
        for next_neighbor in neighbors:
            valid_start = time_ns()
            valid = env.is_valid_for_allocation(next_neighbor, agent)
            valid_time += time_ns() - valid_start
            if valid:
                neighbor = Node(next_neighbor, current_node)

                in_check_start = time_ns()
                # Closed node
                if hash(neighbor) in closed_nodes:
                    continue
                in_check_t += time_ns() - in_check_start

                neighbor.g = current_node.g + 0.5
                neighbor.h = distance2(neighbor.position, end_node.position)
                neighbor.f = neighbor.g + neighbor.h - neighbor.position.y / env.get_dim().y * 0.05 * neighbor.h

                if hash(neighbor) in open_nodes:
                    if open_nodes[hash(neighbor)].f > neighbor.f:
                        open_nodes[hash(neighbor)] = neighbor
                else:
                    open_nodes[hash(neighbor)] = neighbor
        neighbors_time += time_ns() - start_neighbors

    if len(path) == 0:
        print("ASTAR failed")

        # print(len(open_nodes))
        # print(len(closed_nodes))
    print(str(start))
    print(str(end))
    wait_coords: List[TimeCoordinate] = []
    for near_coord in path:
        for t in range(1, agent.speed):
            wait_coords.append(TimeCoordinate(near_coord.x, near_coord.y, near_coord.z, near_coord.t + Tick(t)))

    complete_path = path + wait_coords
    complete_path.sort(key=lambda x: x.t)
    stop_time = time_ns()
    seconds = (stop_time - start_time) / 1e9
    # print(start.inter_temporal_distance(end) / (len(path) + 1))
    print(f"PathLen: {len(path)}, "
          f"steps: {steps}, "
          f"time: {seconds:.2f}s, "
          f"t/p: {seconds / (len(path) + 1):.4f}s, "
          f"sort: {sort_time/1e9:.2f}s, "
          f"neighbours: {neighbors_time/1e9:.2f}s, "
          f"valid: {valid_time/1e9:.2f}s, "
          f"in_check: {in_check_t/1e9:.2f}s, "
          f"in_check_2: {in_check_2_t/1e9:.2f}s ")
    return complete_path


def distance(start: TimeCoordinate, end: TimeCoordinate):
    return abs(start.x - end.x) + abs(start.y - end.y) + abs(start.z - end.z)

def distance15(start: TimeCoordinate, end: TimeCoordinate):
    return math.pow(abs(start.x - end.x) ** 2 + abs(start.y - end.y) ** 2 + abs(start.z - end.z) ** 2, 0.333)

def distance2(start: TimeCoordinate, end: TimeCoordinate):
    return math.pow((start.x - end.x) ** 2 + (start.y - end.y) ** 2 + (start.z - end.z) ** 2, 0.5)

def distance3(start: TimeCoordinate, end: TimeCoordinate):
    return math.pow((start.x - end.x) ** 4 + (start.y - end.y) ** 4 + (start.z - end.z) ** 4, 1/4)

class Node:
    def __init__(self, position: TimeCoordinate, parent):
        self.position = position
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position.x == other.position.y and \
            self.position.y == other.position.y and \
            self.position.z == other.position.z and \
            self.position.t == other.position.t
        # return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash(self.position)

    def __repr__(self):
        return f"{self.position}: {self.f}, {self.h}"

    def adjacent_coordinates(self, dim: Coordinate, speed: int) -> List[TimeCoordinate]:
        res = [TimeCoordinate(self.position.x, self.position.y, self.position.z, Tick(
            self.position.t + speed))]
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
