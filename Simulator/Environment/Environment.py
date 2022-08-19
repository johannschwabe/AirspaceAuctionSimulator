from typing import List, Dict, TYPE_CHECKING, Optional, Literal

from rtree import index, Index

from ..Agents.PathAgents.PathAgent import PathAgent
from ..Agents.SpaceAgents.SpaceAgent import SpaceAgent
from ..Blocker.BlockerType import BlockerType
from ..Path.PathAllocation import PathAllocation
from ..Path.SpaceAllocation import SpaceAllocation

if TYPE_CHECKING:
    from ..Blocker.Blocker import Blocker
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Agents.Agent import Agent
    from ..Path.Allocation import Allocation
    from ..Path.PathSegment import PathSegment
    from ..Path.SpaceSegment import SpaceSegment


class Environment:
    def __init__(self,
                 dimension: "Coordinate4D",
                 blockers: Optional[List["Blocker"]] = None,
                 min_height: int = 5,
                 allocation_period: int = 50,
                 _tree: Optional[Index] = None,
                 _blocker_tree: Optional[Index] = None):

        self.dimension: "Coordinate4D" = dimension
        self.min_height = min_height
        self.allocation_period = allocation_period

        if blockers is None:
            blockers = []

        self.blocker_dict: Dict[int, "Blocker"] = {}
        self._blocker_id = 0
        for blocker in blockers:
            blocker.id = self.get_blocker_id()
            self.blocker_dict[blocker.id] = blocker

        if _blocker_tree is None:
            self.blocker_tree = self.setup_rtree()
            for blocker in blockers:
                blocker.add_to_tree(self.blocker_tree, self.dimension)
        else:
            self.blocker_tree = _blocker_tree

        if _tree is None:
            self.tree = self.setup_rtree()
        else:
            self.tree = _tree

        self.agents: Dict[int, "Agent"] = {}

        self.max_near_radius = 0
        self.max_far_radius = 0

    @staticmethod
    def setup_rtree() -> Index:
        props = index.Property()
        props.dimension = 4
        return index.Rtree(properties=props)

    def get_blocker_id(self) -> int:
        blocker_id = self._blocker_id
        self._blocker_id += 1
        return blocker_id

    def deallocate_agent(self, agent: "Agent", time_step: int):
        if isinstance(agent, PathAgent):
            self.deallocate_path_agent(agent, time_step)
        elif isinstance(agent, SpaceAgent):
            self.deallocate_space_agent(agent, time_step)
        else:
            raise Exception(f"Unknown agent class {agent.__class__}")

    def deallocate_path_agent(self, agent: "PathAgent", time_step: int):
        new_segments = []
        for path_segment in agent.allocated_segments:
            if path_segment.max.t <= time_step:
                new_segments.append(path_segment)
            else:
                if path_segment.min.t < time_step:
                    first, second = path_segment.split_temporal(time_step)
                    new_segments.append(first)
                    for coordinate in second.coordinates:
                        self.tree.delete(agent.id, coordinate.tree_query_point_rep())
                else:
                    for coordinate in path_segment.coordinates:
                        self.tree.delete(agent.id, coordinate.tree_query_point_rep())

        agent.allocated_segments = new_segments

    def deallocate_space_agent(self, agent: "SpaceAgent", time_step: int):
        new_segments = []
        for space_segment in agent.allocated_segments:
            if space_segment.max.t <= time_step:
                new_segments.append(space_segment)
            else:
                self.tree.delete(agent.id, space_segment.tree_rep())
                if space_segment.min.t < time_step:
                    first, _ = space_segment.split_temporal(time_step)
                    new_segments.append(first)
                    self.tree.insert(agent.id, first)

        agent.allocated_segments = new_segments

    def allocate_path_for_agent(self, agent: "PathAgent", path: List["PathSegment"]):
        for path_segment in path:
            self.allocate_path_segment_for_agent(agent, path_segment)

    def allocate_space_for_agent(self, agent: "SpaceAgent", spaces: List["SpaceSegment"]):
        for space in spaces:
            self.allocate_space_segment_for_agent(agent, space)

    def allocate_path_segment_for_agent(self, agent: "PathAgent", path_segment: "PathSegment"):
        agent.add_allocated_segment(path_segment)
        for coord in path_segment.coordinates:
            self.tree.insert(agent.id, coord.tree_query_point_rep())

    def allocate_space_segment_for_agent(self, agent: "SpaceAgent", space_segment: "SpaceSegment"):
        agent.add_allocated_segment(space_segment)
        self.tree.insert(agent.id, space_segment.tree_rep())

    def allocate_segments_for_agents(self,
                                     real_allocations: List["Allocation"],
                                     time_step: int):
        for allocation in real_allocations:
            if isinstance(allocation, SpaceAllocation):
                agent: "SpaceAgent" = allocation.agent
                segments: List["SpaceSegment"] = allocation.segments
                self.register_agent(agent, time_step)
                self.allocate_space_for_agent(agent, segments)

            elif isinstance(allocation, PathAllocation):
                agent: "PathAgent" = allocation.agent
                segments: List["PathSegment"] = allocation.segments
                self.register_agent(agent, time_step)
                self.allocate_path_for_agent(agent, segments)
            else:
                raise Exception(f"Unknown allocation class {allocation.__class__}")

    def register_agent(self, agent: "Agent", time_step: int):
        if agent.id in self.agents:
            self.deallocate_agent(agent, time_step)
        else:
            self.agents[agent.id] = agent

    def create_real_allocations(self,
                                temporary_allocations: List["Allocation"],
                                new_agents: Dict[int, "Agent"]) -> List["Allocation"]:
        res = []
        for temporary_allocation in temporary_allocations:
            new_agent_id = temporary_allocation.agent.id
            if new_agent_id in new_agents:
                res.append(temporary_allocation.correct_agent(new_agents[new_agent_id]))
            else:
                res.append(temporary_allocation.correct_agent(self.agents[new_agent_id]))
        return res

    def get_blockers(self, coord: "Coordinate4D", radius: int, speed: int) -> List[int]:
        return list(self.blocker_tree.intersection(coord.tree_query_qube_rep(radius, speed)))

    def is_blocked(self, coord: "Coordinate4D", radius: int = 0, speed: int = 0) -> bool:
        for blocker_id in self.get_blockers(coord, radius, speed):
            blocker = self.blocker_dict[blocker_id]
            if blocker.is_blocking(coord, radius):
                return True
        return False

    def is_blocked_forever(self, coord: "Coordinate4D", radius: int = 0, speed: int = 0) -> bool:
        for blocker_id in self.get_blockers(coord, radius, speed):
            blocker = self.blocker_dict[blocker_id]
            if blocker.blocker_type == BlockerType.STATIC.value and blocker.is_blocking(coord, radius):
                return True
        return False

    def is_blocked_by_agent(self, coord: "Coordinate4D", agent: "PathAgent") -> bool:
        intersections_large = self.intersect(coord, self.max_near_radius, agent.speed)
        intersections_small = self.intersect(coord, agent.near_radius, agent.speed)
        for intersection_id in intersections_large:
            if intersection_id == agent.id:
                continue
            colliding_agent = self.get_agent(intersection_id)
            if isinstance(colliding_agent, PathAgent):
                allocated_segments = colliding_agent.allocated_segments
                count = 0
                while allocated_segments[count].coordinates[-1].t < coord.t:
                    count += 1
                colliding_segment = allocated_segments[count].coordinates
                collision = colliding_segment[coord.t - colliding_segment[0].t]
                distance = coord.distance(collision)
                if distance <= agent.near_radius or colliding_agent.near_radius <= distance:
                    return False
            else:
                if intersection_id in intersections_small:
                    return False

    def is_box_blocked(self, bottom_left: "Coordinate4D", top_right: "Coordinate4D") -> bool:
        blockers = self.blocker_tree.intersection((
            bottom_left.list_rep() +
            top_right.list_rep()
        ))
        for blocker_id in blockers:
            if self.blocker_dict[blocker_id].is_box_blocking(bottom_left, top_right):
                return True
        return False

    def add_agent(self, agent: "Agent"):
        self.agents[agent.id] = agent
        if isinstance(agent, PathAgent):
            self.max_near_radius = max(self.max_near_radius, agent.near_radius)
            self.max_far_radius = max(self.max_far_radius, agent.far_radius)

    def get_agent(self, agent_id: int):
        return self.agents[agent_id]

    def is_valid_for_allocation(self, coords: "Coordinate4D", agent: "Agent") -> bool:
        if isinstance(agent, PathAgent):
            radius: int = agent.near_radius
            agents = self.intersect(coords, radius, agent.speed)
            return len(list(agents)) == 0 and not self.is_blocked(coords, radius, agent.speed)
        elif isinstance(agent, SpaceAgent):
            agents = self.intersect(coords, 0, 0)
            return len(list(agents)) == 0 and not self.is_blocked(coords, 0, 0)

    def is_box_valid_for_allocation(self,
                                    bottom_left: "Coordinate4D",
                                    top_right: "Coordinate4D",
                                    agent: "SpaceAgent") -> bool:
        agents = self.intersect_box(bottom_left, top_right, "raw")
        agent_free = len([_agent for _agent in agents if agent.id != _agent]) == 0
        blocker_free = self.is_box_blocked(bottom_left, top_right)
        return agent_free and blocker_free

    def intersect_box(self, mini: "Coordinate4D", maxi: "Coordinate4D", _objects: bool | Literal["raw"] = True):
        return self.tree.intersection(mini.list_rep() + maxi.list_rep(), objects=_objects)

    def can_be_valid_for_allocation(self, coords: "Coordinate4D", agent: "Agent") -> bool:
        if isinstance(agent, PathAgent):
            return not self.is_blocked_forever(coords, agent.near_radius, agent.speed)
        elif isinstance(agent, SpaceAgent):
            return not self.is_blocked_forever(coords, 0, 0)

    def intersect(self, coords: "Coordinate4D", radius: int = 0, speed: int = 0):
        return self.tree.intersection(coords.tree_query_qube_rep(radius, speed))

    def new_clear(self):
        new_env = Environment(self.dimension,
                              list(self.blocker_dict.values()),
                              min_height=self.min_height,
                              allocation_period=self.allocation_period,
                              _blocker_tree=self.blocker_tree)
        return new_env

    def clone(self):
        cloned_tree: "Index" = self.setup_rtree()
        if len(self.tree) > 0:
            all_items = self.tree.intersection(self.tree.bounds, objects=True)
            for item in all_items:
                cloned_tree.insert(item.id, item.bbox)

        cloned = Environment(self.dimension,
                             list(self.blocker_dict.values()),
                             min_height=self.min_height,
                             allocation_period=self.allocation_period,
                             _tree=cloned_tree,
                             _blocker_tree=self.blocker_tree)

        for agent in self.agents.values():
            cloned.add_agent(agent.clone())

        return cloned
