import math
from typing import Iterator, Optional, Set, TYPE_CHECKING, Tuple

from rtree import Index
from rtree.index import Item, Property

from Simulator.Agents.PathAgent import PathAgent
from Simulator.Agents.SpaceAgent import SpaceAgent

if TYPE_CHECKING:
    from Simulator.Bids.BidTracker import BidTracker
    from Simulator.Coordinates.Coordinate4D import Coordinate4D
    from Simulator.Environment.Environment import Environment
    from Simulator.Agents.Agent import Agent


def find_valid_path_tick(tick: int, environment: "Environment", bid_tracker: "BidTracker", position: "Coordinate4D",
                         agent: "PathAgent", min_tick: int, max_tick: int) -> Optional[int]:
    """
    Checks if the given position is valid to allocate.
    If not, it tries to find a later tick where an allocation is possible.
    The returned tick is in the range [max{position.t, min_tick}, max_tick] or None if no valid tick is found.
    :param tick: the current simulation tick
    :param environment: the environment in which to find a valid allocation
    :param bid_tracker: the bid-tracker to get past and new agent bids
    :param position: the position at which to find a valid allocation tick
    :param agent: the agent that should be allocated
    :param min_tick: the minimum tick of the range in which the allocation must be
    :param max_tick: the maximum tick of the range in which the allocation must be
    :return: tick in the range [max{position.t, min_tick}, max_tick] or None
    """
    pos_clone = position.clone()
    if pos_clone.t < min_tick:
        pos_clone.t = min_tick
    while True:
        valid, _ = is_valid_for_path_allocation(tick, environment, bid_tracker, pos_clone, agent)
        if pos_clone.t > max_tick:
            return None
        if valid:
            break
        pos_clone.t += 1

    return pos_clone.t


def find_valid_space_tick(tick: int, environment: "Environment", bid_tracker: "BidTracker",
                          min_position: "Coordinate4D", max_position: "Coordinate4D", agent: "SpaceAgent",
                          min_tick: int, max_tick: int, avoid_blockers: bool = False) -> Optional[int]:
    """
    Checks if the given space is valid to allocate.
    If not, it tries to find a later tick where an allocation is possible.
    The returned tick is in the range [max{min_position.t, min_tick}, min{max_position.t, max_tick}] or None if no
    valid tick is found.
    :param tick: the current simulation tick
    :param environment: the environment in which to find a valid allocation
    :param bid_tracker: the bid-tracker to get past and new agent bids
    :param min_position: the minimum coordinate of the space for which to find a valid allocation tick
    :param max_position: the maximum coordinate of the space for which to find a valid allocation tick
    :param agent: the agent that should be allocated
    :param min_tick: the minimum tick of the range in which the allocation must be
    :param max_tick: the maximum tick of the range in which the allocation must be
    :param avoid_blockers: if True, it is not allowed to allocate space containing blocker
    :return: tick in the range [max{min_position.t, min_tick}, min{max_position.t, max_tick}] or None
    """
    min_pos_clone = min_position.clone()
    if min_pos_clone.t < min_tick:
        min_pos_clone.t = min_tick
    while True:
        if min_pos_clone.t > max_tick or min_pos_clone.t > max_position.t:
            return None
        valid, _ = is_valid_for_space_allocation(tick, environment, bid_tracker, min_pos_clone, max_position, agent,
                                                 avoid_blockers=avoid_blockers)
        if valid:
            break
        min_pos_clone.t += 1

    return min_pos_clone.t


def is_valid_for_space_allocation(allocation_tick: int,
                                  environment: "Environment",
                                  bid_tracker: "BidTracker",
                                  min_position: "Coordinate4D",
                                  max_position: "Coordinate4D",
                                  space_agent: "SpaceAgent",
                                  avoid_blockers: bool = False) -> Tuple[bool, Optional[Set["Agent"]]]:
    """
    Checks if the given space is valid to allocate.
    :param allocation_tick: the current simulation tick
    :param environment: the environment in which to find a valid allocation
    :param bid_tracker: the bid-tracker to get past and new agent bids
    :param min_position: the minimum coordinate of the space for which to check for a valid allocation
    :param max_position: the maximum coordinate of the space for which to check for a valid allocation
    :param space_agent: the agent that should be allocated
    :param avoid_blockers: if True, it is not allowed to allocate space containing blocker
    :return: Whether the allocation is valid and a set of agents that need to be reallocated if valid.
    """
    if min_position.t < allocation_tick:
        raise Exception(f"Cannot validate position in the past. Position: {min_position}, Tick: {allocation_tick}.")

    if avoid_blockers and environment.is_space_blocked(min_position, max_position):
        return False, None

    my_bid = bid_tracker.get_last_bid_for_tick(allocation_tick, space_agent, environment)

    if my_bid is None:
        return False, None

    if min_position.t == allocation_tick:
        my_segments = space_agent.get_segments_at_tick(allocation_tick)
        flying = False
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
                distance = path_coordinate.distance_to_space(min_position, max_position)
                if distance <= max_intersecting_agent.near_radius:
                    true_intersecting_agents.add(max_intersecting_agent)
                    break

    for true_intersecting_agent in true_intersecting_agents:
        other_bid = bid_tracker.get_last_bid_for_tick(allocation_tick, true_intersecting_agent, environment)
        if other_bid is None:
            raise Exception(f"Agent stuck: {true_intersecting_agent}")

        if my_bid <= other_bid:
            return False, None

    return True, true_intersecting_agents


def is_valid_for_path_allocation(allocation_tick: int,
                                 environment: "Environment",
                                 bid_tracker: "BidTracker",
                                 position: "Coordinate4D",
                                 path_agent: "PathAgent") -> Tuple[bool, Optional[Set["Agent"]]]:
    """
    Checks if the given position is valid to allocate.
    :param allocation_tick: the current simulation tick
    :param environment: the environment in which to find a valid allocation
    :param bid_tracker: the bid-tracker to get past and new agent bids
    :param position: the position at which to check for a valid allocation
    :param path_agent: the agent that should be allocated
    :return: Whether the allocation is valid and a set of agents that need to be reallocated if valid.
    """

    if environment.is_coordinate_blocked(position, path_agent):
        return False, None

    my_bid = bid_tracker.get_last_bid_for_tick(allocation_tick, path_agent, environment)

    if my_bid is None:
        return False, None

    if position.t == allocation_tick:
        my_pos = path_agent.get_position_at_tick(allocation_tick)
        if my_pos is None or my_pos != position:
            return False, None

    true_intersecting_agents = set()
    max_intersecting_agents = environment.intersect_path_coordinate(position, path_agent)
    for max_intersecting_agent in max_intersecting_agents:
        if isinstance(max_intersecting_agent, PathAgent):
            max_near_radius = max(path_agent.near_radius, max_intersecting_agent.near_radius)
            path_coordinates = max_intersecting_agent.get_positions_at_ticks(position.t,
                                                                             position.t + path_agent.speed - 1)
            assert len(path_coordinates) > 0
            for path_coordinate in path_coordinates:
                distance = position.distance(path_coordinate, l2=True)
                if distance <= max_near_radius:
                    true_intersecting_agents.add(max_intersecting_agent)
                    if not _path_agent_can_escape(path_coordinate, max_intersecting_agent.speed, position,
                                                  allocation_tick,
                                                  max_near_radius):
                        return False, None

        elif isinstance(max_intersecting_agent, SpaceAgent):
            segments = max_intersecting_agent.get_segments_at_ticks(position.t, position.t + path_agent.speed)
            assert len(segments) > 0
            for segment in segments:
                distance = position.distance_to_space(segment.min, segment.max)
                if distance <= path_agent.near_radius:
                    true_intersecting_agents.add(max_intersecting_agent)
                    break

        else:
            raise Exception(f"Invalid agent {max_intersecting_agent}")

    for true_intersecting_agent in true_intersecting_agents:
        other_bid = bid_tracker.get_last_bid_for_tick(allocation_tick, true_intersecting_agent, environment)
        if other_bid is None:
            raise Exception(f"Agent stuck: {true_intersecting_agent}")

        if my_bid <= other_bid:
            return False, None

    return True, true_intersecting_agents


def _path_agent_can_escape(intersecting_coordinate: "Coordinate4D",
                           escaping_agent_speed: "int",
                           new_agent_position: "Coordinate4D",
                           allocation_tick: int,
                           max_near_radius: int):
    time_to_collision = intersecting_coordinate.t - allocation_tick

    agent_distance = new_agent_position.distance(intersecting_coordinate, l2=True)
    escape_distance = max_near_radius - agent_distance
    escape_steps = math.ceil(escape_distance * math.sqrt(2))
    if escape_steps < 0:
        return True
    nr_movements = math.floor(time_to_collision / escaping_agent_speed) - 1
    can_escape = nr_movements > escape_steps
    return can_escape


def setup_rtree(data: Optional[Iterator["Item"]] = None) -> Index:
    """
    Returns a rtree instance with 4 dimensions.
    Used internally by the Environment and Statistics modules.
    """
    props = Property()
    props.dimension = 4
    if data is None:
        return Index(properties=props)
    else:
        return Index(_generate_data(data), properties=props)


def _generate_data(data: Iterator["Item"]):
    for item in data:
        yield item.id, item.bbox, item.object
