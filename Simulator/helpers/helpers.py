import math

from ..Agents.PathAgent import PathAgent
from ..Agents.SpaceAgent import SpaceAgent
from ..BidTracker.BidTracker import BidTracker
from ..Coordinates.Coordinate3D import Coordinate3D
from ..Coordinates.Coordinate4D import Coordinate4D
from ..Environment.Environment import Environment


def is_valid_for_allocation(allocation_tick: int, environment: "Environment", bid_tracker: "BidTracker",
                            position: "Coordinate4D", agent: "PathAgent"):
    if position.t < allocation_tick:
        raise Exception(f"Cannot validate position in the past. Position: {position}, Tick: {allocation_tick}.")

    if environment.is_blocked(position, agent):
        return False, None

    my_bid = bid_tracker.get_last_bid_for_tick(allocation_tick, agent, environment)

    if my_bid is None:
        return False, None

    colliding_agents = set()

    flying = False
    if position.t == allocation_tick:
        my_pos = agent.get_position_at_tick(allocation_tick)
        if my_pos is not None and my_pos == position:
            flying = True
        else:
            return False, None

    max_intersecting_agents = environment.intersect_path_coordinate(position, agent)
    for intersecting_agent in max_intersecting_agents:
        true_intersection = False

        if isinstance(intersecting_agent, PathAgent):
            max_near_radius = max(agent.near_radius, intersecting_agent.near_radius)
            path_coordinates = intersecting_agent.get_positions_at_ticks(position.t, speed=agent.speed)
            assert len(path_coordinates) > 0
            for path_coordinate in path_coordinates:
                distance = position.inter_temporal_distance(path_coordinate, l2=True)
                if distance <= max_near_radius:
                    true_intersection = True
                    break

        elif isinstance(intersecting_agent, SpaceAgent):
            segments = intersecting_agent.get_segments_at_ticks(allocation_tick, agent.speed)
            assert len(segments) > 0
            for segment in segments:
                distance = point_cuboid_distance(position, segment.min, segment.max)
                if distance <= agent.near_radius:
                    true_intersection = True
                    break

        else:
            raise Exception(f"Invalid agent {intersecting_agent}")

        if not true_intersection:
            continue

        if flying:
            colliding_agents.add(intersecting_agent)
            continue

        other_bid = bid_tracker.get_last_bid_for_tick(allocation_tick, intersecting_agent, environment)
        if other_bid is None:
            raise Exception(f"Agent stuck: {intersecting_agent}")

        if my_bid > other_bid:
            colliding_agents.add(intersecting_agent)
        else:
            return False, None

    return True, colliding_agents


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
