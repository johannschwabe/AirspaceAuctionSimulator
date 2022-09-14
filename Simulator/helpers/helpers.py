import math
from typing import Optional

from ..Agents.PathAgent import PathAgent
from ..Agents.SpaceAgent import SpaceAgent
from ..BidTracker.BidTracker import BidTracker
from ..Bids.Bid import Bid
from ..Coordinates.Coordinate3D import Coordinate3D
from ..Coordinates.Coordinate4D import Coordinate4D
from ..Environment.Environment import Environment


def find_valid_path_tick(tick: int, environment: "Environment", bid_tracker: "BidTracker", position: "Coordinate4D",
                         bid: "Bid", min_tick: int, max_tick: int) -> Optional[int]:
    pos_clone = position.clone()
    agent = bid.agent
    assert isinstance(agent, PathAgent)
    if pos_clone.t < min_tick:
        pos_clone.t = min_tick
    while True:
        valid, _ = is_valid_for_path_allocation(tick, environment, bid_tracker, pos_clone, agent)
        if valid:
            break
        pos_clone.t += 1
        if pos_clone.t > max_tick:
            return None
    return pos_clone.t


def find_valid_space_tick(tick: int, environment: "Environment", bid_tracker: "BidTracker",
                          min_position: "Coordinate4D", max_position: "Coordinate4D", bid: "Bid", min_tick: int,
                          max_tick: int) -> Optional[int]:
    min_pos_clone = min_position.clone()
    agent = bid.agent
    assert isinstance(agent, SpaceAgent)
    if min_pos_clone.t < min_tick:
        min_pos_clone.t = min_tick
    while True:
        valid, _ = is_valid_for_space_allocation(tick, environment, bid_tracker, min_pos_clone, max_position, agent)
        if valid:
            break
        min_pos_clone.t += 1
        if min_pos_clone.t > max_tick or min_pos_clone.t > max_position.t:
            return None
    return min_pos_clone.t


def is_valid_for_space_allocation(allocation_tick: int, environment: "Environment", bid_tracker: "BidTracker",
                                  min_position: "Coordinate4D", max_position: "Coordinate4D",
                                  space_agent: "SpaceAgent", avoid_blockers: bool = False):
    if min_position.t < allocation_tick:
        raise Exception(f"Cannot validate position in the past. Position: {min_position}, Tick: {allocation_tick}.")

    if avoid_blockers and environment.is_space_blocked(min_position, max_position):
        return False, None

    my_bid = bid_tracker.get_last_bid_for_tick(allocation_tick, space_agent, environment)

    if my_bid is None:
        return False, None

    flying = False
    if min_position.t == allocation_tick:
        my_segments = space_agent.get_segments_at_tick(allocation_tick)
        if len(my_segments) > 0:
            for my_segment in my_segments:
                if my_segment.min <= min_position and my_segment.max >= max_position:
                    flying = True
                    break
        if not flying:
            return False, None

    true_intersecting_agents = environment.intersect_space_coordinates(min_position, max_position, space_agent,
                                                                       use_max_radius=False)
    max_intersecting_agents = environment.intersect_space_coordinates(min_position, max_position, space_agent)
    for max_intersecting_agent in max_intersecting_agents:
        if max_intersecting_agent not in true_intersecting_agents and isinstance(max_intersecting_agent, PathAgent):
            path_coordinates = max_intersecting_agent.get_positions_at_ticks(min_position.t, max_position.t)
            assert len(path_coordinates) > 0
            for path_coordinate in path_coordinates:
                distance = point_cuboid_distance(path_coordinate, min_position, max_position)
                if distance <= max_intersecting_agent.near_radius:
                    true_intersecting_agents.add(max_intersecting_agent)
                    break

    if not flying:
        for true_intersecting_agent in true_intersecting_agents:
            other_bid = bid_tracker.get_last_bid_for_tick(allocation_tick, true_intersecting_agent, environment)
            if other_bid is None:
                raise Exception(f"Agent stuck: {true_intersecting_agent}")

            if my_bid <= other_bid:
                return False, None

    return True, true_intersecting_agents


def is_valid_for_path_allocation(allocation_tick: int, environment: "Environment", bid_tracker: "BidTracker",
                                 position: "Coordinate4D", path_agent: "PathAgent"):
    if position.t < allocation_tick:
        raise Exception(f"Cannot validate position in the past. Position: {position}, Tick: {allocation_tick}.")

    if environment.is_coordinate_blocked(position, path_agent):
        return False, None

    my_bid = bid_tracker.get_last_bid_for_tick(allocation_tick, path_agent, environment)

    if my_bid is None:
        return False, None

    flying = False
    if position.t == allocation_tick:
        my_pos = path_agent.get_position_at_tick(allocation_tick)
        if my_pos is not None and my_pos == position:
            flying = True
        else:
            return False, None

    true_intersecting_agents = set()
    max_intersecting_agents = environment.intersect_path_coordinate(position, path_agent)
    for max_intersecting_agent in max_intersecting_agents:
        if isinstance(max_intersecting_agent, PathAgent):
            max_near_radius = max(path_agent.near_radius, max_intersecting_agent.near_radius)
            path_coordinates = max_intersecting_agent.get_positions_at_ticks(position.t, position.t + path_agent.speed)
            assert len(path_coordinates) > 0
            for path_coordinate in path_coordinates:
                distance = position.inter_temporal_distance(path_coordinate, l2=True)
                if distance <= max_near_radius:
                    true_intersecting_agents.add(max_intersecting_agent)
                    break

        elif isinstance(max_intersecting_agent, SpaceAgent):
            segments = max_intersecting_agent.get_segments_at_ticks(position.t, position.t + path_agent.speed)
            assert len(segments) > 0
            for segment in segments:
                distance = point_cuboid_distance(position, segment.min, segment.max)
                if distance <= path_agent.near_radius:
                    true_intersecting_agents.add(max_intersecting_agent)
                    break

        else:
            raise Exception(f"Invalid agent {max_intersecting_agent}")

    if not flying:
        for true_intersecting_agent in true_intersecting_agents:
            other_bid = bid_tracker.get_last_bid_for_tick(allocation_tick, true_intersecting_agent, environment)
            if other_bid is None:
                raise Exception(f"Agent stuck: {true_intersecting_agent}")

            if my_bid <= other_bid:
                return False, None

    return True, true_intersecting_agents


def distance_l1(start: "Coordinate4D", end: "Coordinate4D"):
    return abs(start.x - end.x) + abs(start.y - end.y) + abs(start.z - end.z)


def distance_l2(start: "Coordinate4D", end: "Coordinate4D"):
    return math.pow((start.x - end.x) ** 2 + (start.y - end.y) ** 2 + (start.z - end.z) ** 2, 0.5)


def point_cuboid_distance(point: "Coordinate3D", cube_min: "Coordinate3D", cube_max: "Coordinate3D"):
    # x
    if point.x < cube_min.x:
        x = cube_min.x
    elif point.x > cube_max.x:
        x = cube_max.x
    else:
        x = point.x

    # y
    if point.y < cube_min.y:
        y = cube_min.y
    elif point.y > cube_max.y:
        y = cube_max.y
    else:
        y = point.y

    # z
    if point.z < cube_min.z:
        z = cube_min.z
    elif point.z > cube_max.z:
        z = cube_max.z
    else:
        z = point.z

    return math.sqrt(math.pow(x - point.x, 2) + math.pow(y - point.y, 2) + math.pow(z - point.z, 2))
