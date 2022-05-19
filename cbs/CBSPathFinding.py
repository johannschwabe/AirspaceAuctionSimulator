import math
from typing import List, TYPE_CHECKING
from time import time_ns

from Simulator.Agent import Agent
from Simulator.Environment import Environment
from Simulator.Time import Tick
from Simulator.Coordinate import TimeCoordinate, Coordinate



# Implemented based on https://www.annytab.com/a-star-search-algorithm-in-python/
from cbs.CBSHelpers import VertexConstraint, EdgeConstraint


def astar(
    start: TimeCoordinate,
    end: TimeCoordinate,
    env: Environment,
    agent: Agent,
    constraints: "Constraints"
):
    # print(f"{start} -> {end} ---->", end="")
    # print(f"---->", end="")
    start_time = time_ns()
    open_nodes = []
    closed_nodes = []

    valid_start = start
    while not is_valid_for_allocation(env, valid_start, valid_start, agent, constraints):
        valid_start.t += 1

    start_node = Node(start, None)
    end_node = Node(end, None)
    open_nodes.append(start_node)
    steps = 0

    path = []
    sort_time = 0
    neighbors_time = 0
    valid_time = 0
    MAX_ITER = 10000
    while len(open_nodes) > 0 and steps < MAX_ITER:
        steps += 1

        start_sort = time_ns()
        open_nodes.sort()
        sort_time += time_ns() - start_sort

        current_node = open_nodes.pop(0)
        closed_nodes.append(current_node)

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
            valid = is_valid_for_allocation(env, current_node.position, next_neighbor, agent, constraints)
            valid_time += time_ns() - valid_start
            if valid:
                neighbor = Node(next_neighbor, current_node)
                # Closed node
                if neighbor in closed_nodes:
                    break

                neighbor.g = current_node.g + 0.5
                neighbor.h = distance2(neighbor.position, end_node.position)
                neighbor.f = neighbor.g + neighbor.h

                open_nodes.append(neighbor)
        neighbors_time += time_ns() - start_neighbors

    if len(path) == 0:
        print("ASTAR failed")
    wait_coords: List[TimeCoordinate] = []
    for near_coord in path:
        for t in range(1, agent.speed):
            wait_coords.append(TimeCoordinate(near_coord.x, near_coord.y, near_coord.z, near_coord.t + Tick(t)))

    complete_path = path + wait_coords
    complete_path.sort(key=lambda x: x.t)
    stop_time = time_ns()
    seconds = (stop_time - start_time) / 1e9
    # print(f"PathLen: {len(path)}, "
    #       f"steps: {steps}, "
    #       f"time: {seconds:.2f}, "
    #       f"t/p: {seconds / (len(path) + 1) * 1000:.2f}, "
    #       f"sort: {sort_time/1e9:.2f}, "
    #       f"neighbours: {neighbors_time/1e9:.2f}, "
    #       f"valid: {valid_time/1e9:.2f}, ")
    return complete_path


def distance(start: TimeCoordinate, end: TimeCoordinate):
    return abs(start.x - end.x) + abs(start.y - end.y) + abs(start.z - end.z)


def distance2(start: TimeCoordinate, end: TimeCoordinate):
    return math.pow((start.x - end.x) ** 2 + (start.y - end.y) ** 2 + (start.z - end.z) ** 2, 0.5)

def is_valid_for_allocation(env: Environment, field_from: TimeCoordinate, field_to: TimeCoordinate, agent:Agent, constraints):
    env_free = env.is_valid_for_allocation(field_to, agent)
    if not env_free:
        return False
    field_to_cpy = field_to.clone()
    for i in range(agent.speed):
        vertex_constraint_free = VertexConstraint(field_to_cpy) not in constraints.vertex_constraints
        if not vertex_constraint_free:
            return False
        field_to_cpy.t += 1
    field_from_cpy = field_from.clone()
    field_to_cpy = field_to.clone()
    for i in range(agent.speed):
        edge_constraint_free = EdgeConstraint(field_from_cpy, field_to_cpy) not in constraints.edge_constraints
        if not edge_constraint_free:
            return edge_constraint_free
        field_from_cpy = field_from_cpy.clone()
        field_to_cpy.t += 1

    return True
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
