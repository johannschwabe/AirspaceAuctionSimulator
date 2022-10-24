from typing import Dict, Iterator, List, Optional, Set, TYPE_CHECKING, cast

from rtree import Index

from ..Agents.PathAgent import PathAgent
from ..Agents.SpaceAgent import SpaceAgent
from ..Blocker.BlockerType import BlockerType
from ..helpers.helpers import setup_rtree

if TYPE_CHECKING:
    from ..Blocker.Blocker import Blocker
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Agents.Agent import Agent
    from ..Allocations.Allocation import Allocation
    from ..Segments.PathSegment import PathSegment
    from ..Segments.SpaceSegment import SpaceSegment


class Environment:
    def __init__(self,
                 dimension: "Coordinate4D",
                 blockers: Optional[List["Blocker"]] = None,
                 min_height: int = 0):

        self.dimension: "Coordinate4D" = dimension
        self.min_height = min_height

        if blockers is None:
            blockers = []
        self.blocker_dict: Dict[int, "Blocker"] = {}
        self._blocker_id = 0
        self.blocker_tree = setup_rtree()
        for blocker in blockers:
            blocker.id = self._get_blocker_id()
            self.blocker_dict[blocker.id] = blocker
            blocker.add_to_tree(self.blocker_tree, self.dimension)

        self.tree = setup_rtree()
        self.agents: Dict[int, "Agent"] = {}
        self.payments: Dict[int, float] = {}
        self.max_near_radius = 0

    def _get_blocker_id(self) -> int:
        """
        Get the next blocker ID.
        """
        blocker_id = self._blocker_id
        self._blocker_id += 1
        return blocker_id

    def deallocate_agent(self, agent: "Agent", time_step: int):
        """
        Deallocate all future segments of an agent.
        """
        if isinstance(agent, PathAgent):
            self.deallocate_path_agent(agent, time_step)
        elif isinstance(agent, SpaceAgent):
            self.deallocate_space_agent(agent, time_step)
        else:
            raise Exception(f"Unknown agent class {agent.__class__}")

    def deallocate_path_agent(self, agent: "PathAgent", time_step: int):
        """
        Deallocate all future path segments of a path agent.
        """
        new_segments = []
        for path_segment in agent.allocated_segments:
            if path_segment.max.t <= time_step:
                new_segments.append(path_segment)
            else:
                if path_segment.min.t <= time_step:
                    first, _ = path_segment.split_temporal(time_step)
                    new_segments.append(first)
                self.deallocate_path_segment_for_agent(agent, path_segment, time_step)

        agent.allocated_segments = new_segments

    def deallocate_path_segment_for_agent(self, agent: "PathAgent", path_segment: "PathSegment", time_step: int):
        """
        Allocate a path segment.
        """
        min_index = max(time_step - path_segment.min.t, 0)
        for coord in path_segment.coordinates[min_index::agent.speed]:
            intersections = self.tree.intersection(coord.tree_query_point_rep(), objects=True)
            for intersection in intersections:
                _index = intersection.id
                bbox = intersection.bbox
                if _index == hash(agent):
                    self.tree.delete(hash(agent), bbox)
                    if bbox[3] <= int(time_step):
                        bbox[7] = int(time_step)
                        self.tree.insert(hash(agent), bbox)

    def deallocate_space_agent(self, agent: "SpaceAgent", time_step: int):
        """
        Deallocate all future space segments of a space agent.
        """
        new_segments = []
        for space_segment in agent.allocated_segments:
            if space_segment.max.t <= time_step:
                new_segments.append(space_segment)
            else:
                self.tree.delete(hash(agent), space_segment.tree_rep())
                if space_segment.min.t < time_step:
                    first, _ = space_segment.split_temporal(time_step)
                    new_segments.append(first)
                    self.tree.insert(hash(agent), first.tree_rep())

        agent.allocated_segments = new_segments

    def allocate_path_for_agent(self, agent: "PathAgent", path_segments: List["PathSegment"]):
        """
        Allocate path segments for a path agent.
        """
        for path_segment in path_segments:
            self.allocate_path_segment_for_agent(agent, path_segment)

    def allocate_space_for_agent(self, agent: "SpaceAgent", space_segments: List["SpaceSegment"]):
        """
        Allocate space segments for a space agent.
        """
        for space in space_segments:
            self.allocate_space_segment_for_agent(agent, space)

    def allocate_path_segment_for_agent(self, agent: "PathAgent", path_segment: "PathSegment"):
        """
        Allocate a path segment.
        """
        agent.add_allocated_segment(path_segment)
        inter_temporal_equal: List["Coordinate4D"] = []
        for coord in path_segment.coordinates:
            if len(inter_temporal_equal) != 0 and not coord.inter_temporal_equal(inter_temporal_equal[-1]):
                self.tree.insert(hash(agent), inter_temporal_equal[0].list_rep() + inter_temporal_equal[-1].list_rep())
                inter_temporal_equal = []
            inter_temporal_equal.append(coord)

        self.tree.insert(hash(agent), inter_temporal_equal[0].list_rep() + inter_temporal_equal[-1].list_rep())

    def allocate_space_segment_for_agent(self, agent: "SpaceAgent", space_segment: "SpaceSegment"):
        """
        Allocate a space segment.
        """
        agent.add_allocated_segment(space_segment)
        self.tree.insert(hash(agent), space_segment.tree_rep())

    def allocate_segments_for_agents(self,
                                     allocations: List["Allocation"],
                                     time_step: int):
        """
        Allocate according to the given allocation.
        Only reallocates segments that are in the future.
        """
        for allocation in allocations:
            agent = allocation.agent
            segments = allocation.segments
            self.register_or_reset_agent(agent, time_step)

            if isinstance(agent, SpaceAgent):
                space_segments: List['SpaceSegment'] = cast(List['SpaceSegment'], segments)
                self.allocate_space_for_agent(agent, space_segments)

            elif isinstance(agent, PathAgent):
                path_segments: List['PathSegment'] = cast(List['PathSegment'], segments)
                self.allocate_path_for_agent(agent, path_segments)

            else:
                raise Exception(f"Invalid Agent: {agent}")

    def register_or_reset_agent(self, agent: "Agent", time_step: int):
        """
        Register a new (or existing) agent with the environment.
        If the agent already exists, he gets deallocated.
        """
        if hash(agent) in self.agents:
            self.deallocate_agent(agent, time_step)
        else:
            self.add_agent(agent)

    def create_real_allocations(self,
                                temporary_allocations: List["Allocation"],
                                new_agents: Dict[int, "Agent"]) -> List["Allocation"]:
        """
        Accepts a list of allocations with cloned agents and returns a list of allocations with real agents.
        """
        res = []
        for temporary_allocation in temporary_allocations:
            agent_hash: int = hash(temporary_allocation.agent)
            if agent_hash in new_agents:
                res.append(temporary_allocation.get_allocation_with_agent(new_agents[agent_hash]))
            else:
                res.append(temporary_allocation.get_allocation_with_agent(self.agents[agent_hash]))
        return res

    def get_blockers_at_coordinate(self, coord: "Coordinate4D", radius: float, speed: int) -> Set["Blocker"]:
        """
        Returns a list of all blocker IDs that intersect a qube around the given coordinate with size 2 * radius.
        All time steps from coordinate.t to coordinate.t + speed are considered.
        """
        blocker_ids = set(self.blocker_tree.intersection(coord.tree_query_cube_rep(radius, speed)))
        return set([self.blocker_dict[blocker_id] for blocker_id in blocker_ids])

    def get_blockers_in_space(self, min_coord: "Coordinate4D", max_coord: "Coordinate4D") -> Set["Blocker"]:
        """
        Returns a list of all blocker IDs that intersect a space.
        """
        blocker_ids = set(self.blocker_tree.intersection(min_coord.list_rep() + max_coord.list_rep()))
        return set([self.blocker_dict[blocker_id] for blocker_id in blocker_ids])

    def is_coordinate_blocked(self, coord: "Coordinate4D", agent: "PathAgent") -> bool:
        """
        Returns True if there is a blocker at the given coordinate or in its radius.
        All time steps from coordinate.t to coordinate.t + speed are considered.
        The radius is abstracted by a qube around the given coordinate with size 2 * radius.
        """
        for blocker in self.get_blockers_at_coordinate(coord, agent.near_radius, agent.speed):
            if blocker.is_blocking(coord, agent.near_radius):
                return True
        return False

    def is_space_blocked(self, min_coord: "Coordinate4D", max_coord: "Coordinate4D") -> bool:
        """
        Returns True if there is a blocker in the given space.
        """
        for blocker in self.get_blockers_in_space(min_coord, max_coord):
            if blocker.is_box_blocking(min_coord, max_coord):
                return True
        return False

    def is_coordinate_blocked_forever(self, coordinate: "Coordinate4D", radius: float) -> bool:
        """
        Returns True if there is a static blocker at the given coordinate or in its radius.
        The radius is abstracted by a qube around the given coordinate with size 2 * radius.
        """
        for blocker in self.get_blockers_at_coordinate(coordinate, radius, 0):
            if blocker.blocker_type == BlockerType.STATIC.value and blocker.is_blocking(coordinate, radius):
                return True
        return False

    def is_space_blocked_forever(self, min_coordinate: "Coordinate4D", max_coordinate: "Coordinate4D") -> bool:
        """
        Returns True if there is a static blocker at the given coordinate or in its radius.
        The radius is abstracted by a qube around the given coordinate with size 2 * radius.
        """
        for blocker in self.get_blockers_in_space(min_coordinate, max_coordinate):
            if blocker.blocker_type == BlockerType.STATIC.value and blocker.is_box_blocking(min_coordinate,
                                                                                            max_coordinate):
                return True
        return False

    def have_intersections_collision(self, coord: "Coordinate4D", agent: "PathAgent", intersections: Set[int],
                                     exclusions: Set[int]) -> bool:
        """
        Returns True if the given intersections have any collisions with the agent.
        The exclusions are not checked. They should be checked before.
        """
        for agent_hash in intersections:
            if agent_hash != agent.id and agent_hash not in exclusions:
                other_agent = self.agents[agent_hash]
                if isinstance(other_agent, PathAgent):
                    if other_agent.does_collide(coord, agent):
                        return True
        return False

    def add_agent(self, agent: "Agent"):
        """
        Add a new agent and record its radii.
        """
        self.agents[hash(agent)] = agent
        if isinstance(agent, PathAgent):
            self.max_near_radius = max(self.max_near_radius, agent.near_radius)

    def other_agents_in_space(self,
                              bottom_left: "Coordinate4D",
                              top_right: "Coordinate4D",
                              agent: "SpaceAgent") -> Set["Agent"]:
        """
        Returns a set of all agents in the given space that are not the given agent.
        """
        intersections: Iterator[int] = self.tree.intersection(bottom_left.list_rep() + top_right.list_rep())
        other_agents: List["Agent"] = [self.agents[intersection_id] for intersection_id in intersections if
                                       intersection_id != hash(agent)]
        return set(other_agents)

    def intersect_space_segment(self, space_segment: "SpaceSegment", space_agent: "SpaceAgent") -> Set["Agent"]:
        """
        Returns all other agent in the space
        """
        agent_hashes = set(self.tree.intersection(space_segment.tree_rep()))
        return set([self.agents[agent_hash] for agent_hash in agent_hashes if agent_hash != hash(space_agent)])

    def intersect_space_coordinates(self,
                                    min_coords: "Coordinate4D",
                                    max_coords: "Coordinate4D",
                                    space_agent: "SpaceAgent",
                                    use_max_radius: bool = True) -> Set["Agent"]:
        """
        Returns all other agents intersecting with the given coordinate.
        The radius is abstracted by a qube around the given coordinate with size 2 * radius.
        """
        min_corner = min_coords - self.max_near_radius if use_max_radius else min_coords
        max_corner = max_coords + self.max_near_radius if use_max_radius else max_coords
        min_corner.t = min_coords.t
        max_corner.t = max_coords.t
        agent_hashes = set(self.tree.intersection(min_corner.list_rep() + max_corner.list_rep()))
        return set([self.agents[agent_hash] for agent_hash in agent_hashes if agent_hash != hash(space_agent)])

    def intersect_path_coordinate(self,
                                  coords: "Coordinate4D",
                                  path_agent: "PathAgent",
                                  include_speed: bool = True,
                                  use_max_radius: bool = True) -> Set["Agent"]:
        """
        Returns all other agents intersecting with the given coordinate.
        All time steps from coordinate.t to coordinate.t + speed are considered.
        The radius is abstracted by a qube around the given coordinate with size 2 * radius.
        """
        speed: int = path_agent.speed - 1 if include_speed else 0
        radius: int = max(path_agent.near_radius, self.max_near_radius) if use_max_radius else path_agent.near_radius
        agent_hashes = set(self.tree.intersection(coords.tree_query_cube_rep(radius, speed)))
        return set([self.agents[agent_hash] for agent_hash in agent_hashes if agent_hash != hash(path_agent)])

    def new_clear(self):
        """
        Returns a new environment without any allocated agents.
        """
        new_env = Environment(self.dimension, min_height=self.min_height)
        new_env.blocker_dict = self.blocker_dict
        new_env._blocker_id = self._blocker_id
        new_env.blocker_tree = self.blocker_tree
        return new_env

    def clone(self):
        """
        Returns a clone of the environment with clones of all agents.
        """
        if len(self.tree) > 0:
            all_items = self.tree.intersection(self.tree.bounds, objects=True)
            cloned_tree: "Index" = setup_rtree(all_items)

        else:
            cloned_tree: "Index" = setup_rtree()

        cloned = Environment(self.dimension, min_height=self.min_height)
        cloned.blocker_dict = self.blocker_dict
        cloned._blocker_id = self._blocker_id
        cloned.tree = cloned_tree
        cloned.blocker_tree = self.blocker_tree
        for agent in self.agents.values():
            cloned.add_agent(agent.clone())

        return cloned
