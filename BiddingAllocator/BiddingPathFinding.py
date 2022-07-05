import math
from typing import List
from time import time_ns

# Implemented based on https://www.annytab.com/a-star-search-algorithm-in-python/
from .BiddingABAgent import BiddingABAgent
from Simulator import Environment
from Simulator.Coordinate import Coordinate4D, Coordinate3D


def bidding_astar(
    start: Coordinate4D,
    end: Coordinate4D,
    env: Environment,
    agent: BiddingABAgent,
    flying: bool
):
    # print(f"{start} -> {end}")
    # print(f"---->", end="")
    start_time = time_ns()
    open_nodes = {}
    closed_nodes = {}

    valid_start = start.clone()
    while True:
        start_conflicts, valid = is_valid_for_allocation(env, valid_start, agent)
        if not valid:
            if flying:
                print("Astar couldn't find valid start")
                return [], set()
            valid_start.t += 1
        else:
            break

    start_node = Node(valid_start, None, start_conflicts)
    end_node = Node(end, None, set())
    open_nodes[hash(start_node)] = start_node
    steps = 0

    path = []
    total_collisions = set()
    sort_time = 0
    neighbors_time = 0
    valid_time = 0
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
                total_collisions = total_collisions.union(current_node.collision)
                current_node = current_node.parent

            reverse_path.append(current_node.position)
            total_collisions.union(current_node.collision)
            path = reverse_path[::-1]
            break

        start_neighbors = time_ns()
        # Find non-occupied neighbor
        neighbors = current_node.adjacent_coordinates(env._dimension, agent.speed)
        for next_neighbor in neighbors:
            valid_start = time_ns()
            collisions, valid = is_valid_for_allocation(env, next_neighbor, agent)
            valid_time += time_ns() - valid_start

            if valid:
                neighbor = Node(next_neighbor, current_node, collisions)
                # Closed node
                if hash(neighbor) in closed_nodes:
                    break

                neighbor.g = current_node.g + 0.5
                neighbor.h = distance2(neighbor.position, end_node.position)
                neighbor.f = neighbor.g + neighbor.h - neighbor.position.y / env.get_dim().y * 0.05 * neighbor.h

                if hash(neighbor) in open_nodes:
                    if open_nodes[hash(neighbor)].f > neighbor.f:
                        open_nodes[hash(neighbor)] = neighbor
                else:
                    open_nodes[hash(neighbor)] = neighbor

    if len(path) == 0:
        print(f"ASTAR failed for agent: {agent.id}")
    wait_coords: List[Coordinate4D] = []
    for near_coord in path:
        for t in range(1, agent.speed):
            wait_coords.append(Coordinate4D(near_coord.x, near_coord.y, near_coord.z, near_coord.t + Tick(t)))

    complete_path = path + wait_coords
    complete_path.sort(key=lambda x: x.t)
    # stop_time = time_ns()
    # seconds = (stop_time - start_time) / 1e9
    # print(f"PathLen: {len(path)}, "
    #       f"steps: {steps}, "
    #       f"time: {seconds:.2f}, "
    #       f"t/p: {seconds / (len(path) + 1) * 1000:.2f}, "
    #       f"sort: {sort_time/1e9:.2f}, "
    #       f"neighbours: {neighbors_time/1e9:.2f}, "
    #       f"valid: {valid_time/1e9:.2f}, ")
    return complete_path, total_collisions


def distance(start: Coordinate4D, end: Coordinate4D):
    return abs(start.x - end.x) + abs(start.y - end.y) + abs(start.z - end.z)


def distance2(start: Coordinate4D, end: Coordinate4D):
    return math.pow((start.x - end.x) ** 2 + (start.y - end.y) ** 2 + (start.z - end.z) ** 2, 0.5)


def is_valid_for_allocation(env: Environment, position: Coordinate4D, agent: BiddingABAgent):
    if env.is_blocked(position, agent.near_radius, agent.speed):
        return set(), False
    agents = env.intersect(position, agent.near_radius, agent.speed)
    res = set()
    for agent_id in agents:
        if agent_id == agent.id:
            continue
        colliding_agent = env.get_agent(agent_id)
        if colliding_agent.priority < agent.priority:
            res.add(colliding_agent)
        else:
            return set(), False
    return res, True


class Node:
    def __init__(self, position: Coordinate4D, parent, collision: set[BiddingABAgent]):
        self.position = position
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost
        self.collision = collision

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash(self.position)

    def __repr__(self):
        return f"{self.position}: {self.f}, {self.h}"

    def adjacent_coordinates(self, dim: Coordinate3D, speed: int) -> List[Coordinate4D]:
        res = [Coordinate4D(self.position.x, self.position.y, self.position.z,
                            self.position.t + speed)]
        if self.position.x > 0:
            res.append(Coordinate4D(self.position.x - 1, self.position.y, self.position.z,
                                    self.position.t + speed))
        if self.position.y > 0:
            res.append(Coordinate4D(self.position.x, self.position.y - 1, self.position.z,
                                    self.position.t + speed))
        if self.position.z > 0:
            res.append(Coordinate4D(self.position.x, self.position.y, self.position.z - 1,
                                    self.position.t + speed))
        if self.position.x < dim.x - 1:
            res.append(Coordinate4D(self.position.x + 1, self.position.y, self.position.z,
                                    self.position.t + speed))
        if self.position.y < dim.y - 1:
            res.append(Coordinate4D(self.position.x, self.position.y + 1, self.position.z,
                                    self.position.t + speed))
        if self.position.z < dim.z - 1:
            res.append(Coordinate4D(self.position.x, self.position.y, self.position.z + 1,
                                    self.position.t + speed))
        return res
