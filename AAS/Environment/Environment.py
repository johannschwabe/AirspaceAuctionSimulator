from typing import List, Dict, TYPE_CHECKING, Optional, Literal

from rtree import index

from ..Agents.PathAgents.PathAgent import PathAgent
from ..Agents.SpaceAgents.SpaceAgent import SpaceAgent
from ..Blocker.BlockerType import BlockerType
from ..Path.PathSegment import PathSegment

if TYPE_CHECKING:
    from ..Blocker.Blocker import Blocker
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Agents.Agent import Agent
    from ..Path.SpaceSegment import SpaceSegment


class Environment:
    def __init__(self,
                 dimension: "Coordinate4D",
                 blockers: Optional[List["Blocker"]] = None,
                 min_height: int = 5,
                 allocation_period: int = 50):
        if blockers is None:
            blockers = []
        self.allocation_period = allocation_period
        self._dimension: "Coordinate4D" = dimension
        self._agents: Dict[int, "Agent"] = {}
        self.blockers: Dict[int, "Blocker"] = {blocky.id: blocky for blocky in blockers}

        props = index.Property()
        props.dimension = 4
        self.tree = index.Rtree(properties=props)
        self._blocker_id = 0
        self.blocker_tree = None
        self.min_height = min_height
        self.max_near_field_radius = 0

    def get_blocker_id(self) -> int:
        blocker_id = self._blocker_id
        self._blocker_id += 1
        return blocker_id

    @staticmethod
    def init(dimension: "Coordinate4D",
             blockers: Optional[List["Blocker"]] = None,
             min_height: int = 5,
             allocation_period: int = 50):
        env = Environment(dimension, blockers, min_height, allocation_period)
        env.init_blocker_tree()
        return env

    def deallocate_agent(self, agent: "Agent", time_step: int):
        if isinstance(agent, PathAgent):
            self.deallocate_path_agent(agent, time_step)
        elif isinstance(agent, SpaceAgent):
            self.deallocate_space_agent(agent, time_step)
        else:
            raise Exception("You gufed")

    def deallocate_path_agent(self, agent: "PathAgent", time_step: int):
        for path_segment in agent.allocated_segments:
            if path_segment[-1].t > time_step:
                for coord in path_segment[max(time_step - path_segment[0].t, 0):]:
                    intersections = self.tree.intersection(coord.tree_query_point_rep(), objects=True)
                    for intersection in intersections:
                        _index = intersection.id
                        bbox = intersection.bbox
                        if _index == agent.id:
                            self.tree.delete(agent.id, bbox)
                        if bbox[3] < int(time_step):
                            bbox[7] = int(time_step)
                            self.tree.insert(agent.id, bbox)

        new_allocated_paths = []
        for path in agent.allocated_segments:
            if path[0].t > time_step:
                break
            if path[-1].t > time_step:
                sub_path = path[:time_step - path[0].t + 1]
                new_allocated_paths.append(PathSegment(path.start, path.end, path.index, sub_path))
            else:
                new_allocated_paths.append(path)
        agent.allocated_segments = new_allocated_paths

    def deallocate_space_agent(self, agent: "SpaceAgent", time_step: int):
        pass

    def init_blocker_tree(self):
        props = index.Property()
        props.dimension = 4
        self.blocker_tree = index.Rtree(properties=props)
        for blocker in self.blockers.values():
            blocker.add_to_tree(self.blocker_tree, self.dimension, self.get_blocker_id())

    def allocate_path_for_agent(self, agent: "PathAgent", path: List[PathSegment]):
        for path_segment in path:
            self.allocate_path_segment_for_agent(agent, path_segment)

    def allocate_spaces_for_agent(self, agent: "SpaceAgent", spaces: List["SpaceSegment"]):
        for space in spaces:
            self.allocate_space_for_agent(agent, space)

    def allocate_path_segment_for_agent(self, agent: "PathAgent", path_segment: PathSegment):
        if len(path_segment) == 0:
            return
        agent.add_allocated_segment(path_segment)
        iterator = path_segment[0]
        for coord in path_segment:
            if coord.inter_temporal_equal(iterator):
                continue
            aggregated = iterator.tree_query_point_rep()
            aggregated[7] = coord.t - 1
            self.tree.insert(agent.id, aggregated)
            iterator = coord

        aggregated = iterator.tree_query_point_rep()
        aggregated[7] = path_segment[-1].t
        self.tree.insert(agent.id, aggregated)

    def allocate_space_for_agent(self, agent: "SpaceAgent", space: "SpaceSegment"):
        agent.add_allocated_segment(space)
        self.tree.insert(agent.id, space.min.list_rep() + space.max.list_rep())

    def allocate_segments_for_agents(self,
                                     agents_segments: List["PathReallocation | SpaceReallocation"],
                                     time_step: int):
        for reallocation in agents_segments:
            agent = reallocation.agent
            segments = reallocation.segments
            if agent.id in self._agents:
                self.deallocate_agent(agent, time_step)
            else:
                self._agents[agent.id] = agent

            if isinstance(agent, SpaceAgent):
                self.allocate_spaces_for_agent(agent, segments)
            elif isinstance(agent, PathAgent):
                self.allocate_path_for_agent(agent, segments)
            else:
                raise Exception("You gufed")

    def original_agents(self,
                        agents_segments: List["PathReallocation | SpaceReallocation"],
                        newcomers: List["Agent"]) -> List["PathReallocation | SpaceReallocation"]:
        res = []
        for reallocation in agents_segments:
            agent_id = reallocation.agent.id
            newcomer_ids = [_agent.id for _agent in newcomers]
            if agent_id in newcomer_ids:
                res.append(reallocation.correct_agent(newcomers[newcomer_ids.index(agent_id)]))
            else:
                res.append(reallocation.correct_agent(self._agents[agent_id]))
        return res

    def get_blockers(self, coord: "Coordinate4D", radius, speed) -> List[int]:
        return self.blocker_tree.intersection((
            coord.x - radius, coord.y - radius, coord.z - radius, coord.t,
            coord.x + radius, coord.y + radius, coord.z + radius, coord.t + speed,
        ))

    def is_blocked(self, coord: "Coordinate4D", radius: int = 0, speed: int = 0) -> bool:
        for blocker_id in self.get_blockers(coord, radius, speed):
            if self.blockers[blocker_id].is_blocking(coord, radius):
                return True
        return False

    def is_blocked_forever(self, coord: "Coordinate4D", radius: int = 0, speed: int = 0) -> bool:
        for blocker_id in self.get_blockers(coord, radius, speed):
            blocker = self.blockers[blocker_id]
            if blocker.blocker_type == BlockerType.STATIC.value and blocker.is_blocking(coord, radius):
                return True
        return False

    def is_blocked_by_agent(self, coord: "Coordinate4D", agent: "PathAgent") -> bool:
        intersections_large = self.intersect(coord, self.max_near_field_radius, agent.speed)
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
            if self.blockers[blocker_id].is_box_blocking(bottom_left, top_right):
                return True
        return False

    def add_agent(self, agent: "Agent"):
        self._agents[agent.id] = agent
        if isinstance(agent, PathAgent):
            self.max_near_field_radius = max(self.max_near_field_radius, agent.near_radius)

    def get_agents(self):
        return self._agents

    def get_agent(self, agent_id: int):
        return self._agents[agent_id]

    def get_dim(self):
        return self._dimension

    def is_valid_for_allocation(self, coords: "Coordinate4D", agent: "Agent") -> bool:
        if isinstance(agent, PathAgent):
            radius: int = agent.near_radius
            agents = self.intersect(coords, radius, agent.speed)
            return len(list(agents)) == 0 and not self.is_blocked(coords, radius, agent.speed)
        elif isinstance(agent, SpaceAgent):
            agents = self.intersect(coords, 0, 0)
            return len(list(agents)) == 0 and not self.is_blocked(coords, 0, 0)

    def is_box_valid_for_allocation(self, bottom_left: "Coordinate4D", top_right: "Coordinate4D",
                                    agent: "SpaceAgent") -> bool:
        agents = self.intersect_box(bottom_left, top_right, "raw")
        agent_free = len([_agent for _agent in agents if agent.id != _agent]) == 0
        blocker_free = self.is_box_blocked(bottom_left, top_right)
        return agent_free and blocker_free

    def intersect_box(self, mini: "Coordinate4D", maxi: "Coordinate4D", _objects: bool | Literal["raw"] = True):
        return self.tree.intersection(mini.list_rep() + maxi.list_rep(), objects=_objects)

    def can_be_valid_for_allocation(self, coords: "Coordinate4D", agent: "Agent") -> bool:
        if isinstance(agent, PathAgent):
            radius: int = agent.near_radius
            return not self.is_blocked_forever(coords, radius, agent.speed)
        elif isinstance(agent, SpaceAgent):
            return not self.is_blocked_forever(coords, 0, 0)

    def intersect(self, coords: "Coordinate4D", radius: int = 0, speed: int = 0):
        return self.tree.intersection((
            coords.x - radius, coords.y - radius, coords.z - radius, coords.t,
            coords.x + radius, coords.y + radius, coords.z + radius, coords.t + speed
        ))

    def get_agents_at(self, coords: "Coordinate4D") -> List["Agent"]:
        return [self._agents[_id] for _id in self.tree.intersection(coords.tree_query_point_rep())]

    def new_clear(self):
        new_env = Environment(self._dimension,
                              list(self.blockers.values()),
                              min_height=self.min_height,
                              allocation_period=self.allocation_period)
        new_env.blocker_tree = self.blocker_tree
        return new_env

    def clone(self):
        cloned = Environment(self._dimension,
                             list(self.blockers.values()),
                             min_height=self.min_height,
                             allocation_period=self.allocation_period)
        if len(self.tree) > 0:
            for item in self.tree.intersection(self.tree.bounds, objects=True):
                # TODO: faster deepCopy of tree
                cloned.tree.insert(item.id, item.bbox)
        cloned.blocker_tree = self.blocker_tree
        for agent in self._agents.values():
            cloned.add_agent(agent.clone())
        return cloned

    @property
    def dimension(self):
        return self._dimension
