import statistics
from typing import TYPE_CHECKING, List, Dict, Optional

from rtree import index, Index

from ..Agents.PathAgent import PathAgent
from ..Agents.SpaceAgent import SpaceAgent
from ..Coordinates.Coordinate2D import Coordinate2D
from ..Owners.Owner import Owner
from ..Segments.PathSegment import PathSegment
from ..Segments.SpaceSegment import SpaceSegment

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Simulator import Simulator
    from ..Agents.Agent import Agent


class Statistics:
    """
    Statistics class that generates statistics for a simulation.
    """
    # Path Statistics
    PATH_L1_DISTANCE = "l1_distance"
    PATH_L2_DISTANCE = "l2_distance"
    PATH_L1_GROUND_DISTANCE = "l1_ground_distance"
    PATH_L2_GROUND_DISTANCE = "l2_ground_distance"
    PATH_HEIGHT_DIFFERENCE = "height_difference"
    PATH_TIME_DIFFERENCE = "time_difference"
    PATH_ASCENT = "ascent"
    PATH_DESCENT = "descent"
    PATH_DISTANCE_TRAVELED = "distance_traveled"
    PATH_GROUND_DISTANCE_TRAVELED = "ground_distance_traveled"
    PATH_MEAN_HEIGHT = "mean_height"
    PATH_MEDIAN_HEIGHT = "median_height"

    # Space Statistics
    SPACE_VOLUME = "volume"
    SPACE_MEAN_VOLUME = "mean_volume"
    SPACE_MEDIAN_VOLUME = "median_volume"
    SPACE_HEIGHT = "height"
    SPACE_MEAN_HEIGHT = "mean_height"
    SPACE_MEDIAN_HEIGHT = "median_height"
    SPACE_AREA = "area"
    SPACE_MEAN_AREA = "mean_area"
    SPACE_MEDIAN_AREA = "median_area"
    SPACE_TIME = "time"
    SPACE_MEAN_TIME = "mean_time"
    SPACE_MEDIAN_TIME = "median_time"
    SPACE_HEIGHT_ABOVE_GROUND = "height_above_ground"
    SPACE_MEAN_HEIGHT_ABOVE_GROUND = "mean_height_above_ground"
    SPACE_MEDIAN_HEIGHT_ABOVE_GROUND = "median_height_above_ground"
    PATH_HEIGHTS = "heights"

    # Agent Violations
    PATH_VIOLATIONS = "path_violations"
    SPACE_VIOLATIONS = "space_violations"
    TOTAL_PATH_VIOLATIONS = "total_path_violations"
    TOTAL_SPACE_VIOLATIONS = "total_space_violations"

    def __init__(self, sim: "Simulator"):
        """
        Simulation instance.
        :param sim:
        """
        self.sim: "Simulator" = sim
        assert sim.time_step == sim.environment.dimension.t + 1

        self.non_colliding_values: Dict["Agent", float] = {}
        self.values: Dict[Agent, float] = {}

    def get_non_colliding_value_for_agent(self, agent: "Agent"):
        """
        Calculate the value for an allocation on an empty map (no other agents).
        :param agent:
        :return:
        """
        if agent not in self.non_colliding_values:
            local_agent = agent.initialize_clone()
            local_env = self.sim.environment.new_clear()
            allocation = self.sim.mechanism.do([local_agent], local_env, 0)[local_agent]
            self.non_colliding_values[agent] = local_agent.value_for_segments(allocation.segments)
        return self.non_colliding_values[agent]

    def get_value_for_agent(self, agent: "Agent"):
        """
        Calculate the value for the allocated segments of an agent.
        :param agent:
        :return:
        """
        if agent not in self.values:
            self.values[agent] = agent.get_allocated_value()
        return self.values[agent]

    def get_total_non_colliding_value(self):
        """
        Calculate the value for the allocations of all agents on an empty map summed up.
        :return:
        """
        total_value = 0
        for agent in self.sim.environment.agents.values():
            total_value += self.get_non_colliding_value_for_agent(agent)
        return total_value

    def get_total_value(self):
        """
        Calculate the value for the allocations of all agents summed up.
        :return:
        """
        total_value = 0
        for agent in self.sim.environment.agents.values():
            total_value += self.get_value_for_agent(agent)
        return total_value

    def get_total_non_colliding_value_for_owner(self, owner: "Owner"):
        """
        Calculate the value for the allocations of all agents of an owner on an empty map summed up.
        :param owner:
        :return:
        """
        total_value = 0
        for agent in owner.agents:
            total_value += self.get_non_colliding_value_for_agent(agent)
        return total_value

    def get_total_value_for_owner(self, owner: "Owner"):
        """
        Calculate the value for the allocations of all agents of an owner summed up.
        :param owner:
        :return:
        """
        total_value = 0
        for agent in owner.agents:
            total_value += self.get_value_for_agent(agent)
        return total_value

    @staticmethod
    def path_segment_statistics(path_segment: "PathSegment"):
        """
        Create statistics for a path-segment.
        :param path_segment:
        :return:
        """
        delta = path_segment.max - path_segment.min

        l1_distance: int = delta.to_3D().l1
        l2_distance: float = delta.to_3D().l2
        l1_ground_distance: int = delta.to_2D().l1
        l2_ground_distance: float = delta.to_2D().l2
        height_difference: int = path_segment.max.y - path_segment.min.y
        time_difference: int = path_segment.max.t - path_segment.min.t
        heights: List[int] = []
        ascent: int = 0
        descent: int = 0
        distance_traveled: int = 0
        ground_distance_traveled: int = 0
        previous_coordinate: Optional["Coordinate4D"] = None
        for coordinate in path_segment.coordinates:
            if previous_coordinate is not None:
                delta = coordinate - previous_coordinate
                # height
                if delta.y > 0:
                    ascent += delta.y
                elif delta.y < 0:
                    descent += abs(delta.y)
                # distance
                distance_traveled += delta.l1
                ground_distance_traveled += delta.to_2D().l1
            # heights
            heights.append(coordinate.y)
            # update previous coordinate
            previous_coordinate = coordinate

        mean_height: float = statistics.mean(heights)
        median_height: int = statistics.median(heights)

        return {
            Statistics.PATH_L1_DISTANCE: l1_distance,
            Statistics.PATH_L2_DISTANCE: l2_distance,
            Statistics.PATH_L1_GROUND_DISTANCE: l1_ground_distance,
            Statistics.PATH_L2_GROUND_DISTANCE: l2_ground_distance,
            Statistics.PATH_HEIGHT_DIFFERENCE: height_difference,
            Statistics.PATH_TIME_DIFFERENCE: time_difference,
            Statistics.PATH_ASCENT: ascent,
            Statistics.PATH_DESCENT: descent,
            Statistics.PATH_DISTANCE_TRAVELED: distance_traveled,
            Statistics.PATH_GROUND_DISTANCE_TRAVELED: ground_distance_traveled,
            Statistics.PATH_MEAN_HEIGHT: mean_height,
            Statistics.PATH_MEDIAN_HEIGHT: median_height,
            Statistics.PATH_HEIGHTS: heights,
        }

    @staticmethod
    def path_statistics(path: List["PathSegment"]):
        """
        Create statistics for a path (list of path-segments).
        :param path:
        :return:
        """
        l1_distance: int = int(path[0].min.inter_temporal_distance(path[-1].max))
        l2_distance: float = path[0].min.inter_temporal_distance(path[-1].max, l2=True)
        l1_ground_distance: int = int(Coordinate2D.distance(path[0].min, path[-1].max))
        l2_ground_distance: float = Coordinate2D.distance(path[0].min, path[-1].max, l2=True)
        height_difference: int = path[-1].max.y - path[0].min.y
        time_difference: int = path[-1].max.t - path[0].min.t
        heights: List[int] = []
        ascent: int = 0
        descent: int = 0
        distance_traveled: int = 0
        ground_distance_traveled: int = 0
        for path_segment in path:
            path_segment_statistics = Statistics.path_segment_statistics(path_segment)
            heights.extend(path_segment_statistics[Statistics.PATH_HEIGHTS])
            ascent += path_segment_statistics[Statistics.PATH_ASCENT]
            descent += path_segment_statistics[Statistics.PATH_DESCENT]
            distance_traveled += path_segment_statistics[Statistics.PATH_DISTANCE_TRAVELED]
            ground_distance_traveled += path_segment_statistics[Statistics.PATH_GROUND_DISTANCE_TRAVELED]

        mean_height: float = statistics.mean(heights)
        median_height: int = statistics.median(heights)

        return {
            Statistics.PATH_L1_DISTANCE: l1_distance,
            Statistics.PATH_L2_DISTANCE: l2_distance,
            Statistics.PATH_L1_GROUND_DISTANCE: l1_ground_distance,
            Statistics.PATH_L2_GROUND_DISTANCE: l2_ground_distance,
            Statistics.PATH_HEIGHT_DIFFERENCE: height_difference,
            Statistics.PATH_TIME_DIFFERENCE: time_difference,
            Statistics.PATH_ASCENT: ascent,
            Statistics.PATH_DESCENT: descent,
            Statistics.PATH_DISTANCE_TRAVELED: distance_traveled,
            Statistics.PATH_GROUND_DISTANCE_TRAVELED: ground_distance_traveled,
            Statistics.PATH_MEAN_HEIGHT: mean_height,
            Statistics.PATH_MEDIAN_HEIGHT: median_height,
            Statistics.PATH_HEIGHTS: heights,
        }

    @staticmethod
    def space_segment_statistics(space_segment: "SpaceSegment"):
        """
        Create statistics for a space-segment.
        :param space_segment:
        :return:
        """
        delta = space_segment.max - space_segment.min
        volume = delta.volume
        area = delta.area
        height = delta.y
        time = delta.t
        height_above_ground = space_segment.min.y

        return {
            Statistics.SPACE_VOLUME: volume,
            Statistics.SPACE_AREA: area,
            Statistics.SPACE_HEIGHT: height,
            Statistics.SPACE_TIME: time,
            Statistics.SPACE_HEIGHT_ABOVE_GROUND: height_above_ground,
        }

    @staticmethod
    def _setup_rtree() -> Index:
        """
        Returns a rtree instance with 4 dimensions.
        """
        props = index.Property()
        props.dimension = 4
        return index.Rtree(properties=props)

    @staticmethod
    def spaces_statistics(spaces: List["SpaceSegment"]):
        """
        Create statistics for spaces (list of space-segments).
        :param spaces:
        :return:
        """
        summed_volume = 0
        intersecting_volume = 0
        volumes = []
        summed_area = 0
        intersecting_area = 0
        areas = []
        heights = []
        times = []
        heights_above_ground = []

        tree = Statistics._setup_rtree()

        for space_segment in spaces:
            intersections = tree.intersection(space_segment.tree_rep(), objects="raw")
            for intersecting_space_segment in intersections:
                assert isinstance(intersecting_space_segment, SpaceSegment)
                intersecting_space = space_segment.intersect(intersecting_space_segment)
                intersecting_volume += intersecting_space.volume
                intersecting_area += intersecting_space.area

            tree.insert(hash(space_segment), space_segment.tree_rep(), obj=space_segment)

            space_segment_statistics = Statistics.space_segment_statistics(space_segment)
            summed_volume += space_segment_statistics[Statistics.SPACE_VOLUME]
            volumes.append(space_segment_statistics[Statistics.SPACE_VOLUME])
            summed_area += space_segment_statistics[Statistics.SPACE_AREA]
            areas.append(space_segment_statistics[Statistics.SPACE_AREA])
            heights.append(space_segment_statistics[Statistics.SPACE_HEIGHT])
            times.append(space_segment_statistics[Statistics.SPACE_TIME])
            heights_above_ground.append(space_segment_statistics[Statistics.SPACE_HEIGHT_ABOVE_GROUND])

        volume = summed_volume - intersecting_volume
        mean_volume = statistics.mean(volumes)
        median_volume = statistics.median(volumes)
        area = summed_area - intersecting_area
        mean_area = statistics.mean(areas)
        median_area = statistics.median(areas)
        mean_height = statistics.mean(heights)
        median_height = statistics.median(heights)
        mean_time = statistics.mean(times)
        median_time = statistics.median(times)
        mean_height_above_ground = statistics.mean(heights_above_ground)
        median_height_above_ground = statistics.median(heights_above_ground)

        return {
            Statistics.SPACE_VOLUME: volume,
            Statistics.SPACE_MEAN_VOLUME: mean_volume,
            Statistics.SPACE_MEDIAN_VOLUME: median_volume,
            Statistics.SPACE_AREA: area,
            Statistics.SPACE_MEAN_AREA: mean_area,
            Statistics.SPACE_MEDIAN_AREA: median_area,
            Statistics.SPACE_MEAN_HEIGHT: mean_height,
            Statistics.SPACE_MEDIAN_HEIGHT: median_height,
            Statistics.SPACE_MEAN_TIME: mean_time,
            Statistics.SPACE_MEDIAN_TIME: median_time,
            Statistics.SPACE_MEAN_HEIGHT_ABOVE_GROUND: mean_height_above_ground,
            Statistics.SPACE_MEDIAN_HEIGHT_ABOVE_GROUND: median_height_above_ground,
        }

    def agent_violations(self, agent: "Agent"):
        """
        Tracks all violations for the given agent.
        :param agent:
        :return:
        """
        path_violations: Dict["PathAgent", List["Coordinate4D"]] = {}
        space_violations: Dict["SpaceAgent", List["Coordinate4D"]] = {}
        total_path_violations: int = 0
        total_space_violations: int = 0

        for segment in agent.allocated_segments:
            if isinstance(segment, PathSegment):
                assert isinstance(agent, PathAgent)
                segment_encounters = self.path_segment_violations(agent, segment)

            elif isinstance(segment, SpaceSegment):
                segment_encounters = self.space_segment_violations(segment)

            else:
                raise Exception(f"Invalid Segment: {segment}")

            path_violations.update(segment_encounters[Statistics.PATH_VIOLATIONS])
            space_violations.update(segment_encounters[Statistics.SPACE_VIOLATIONS])
            total_path_violations += segment_encounters[Statistics.TOTAL_PATH_VIOLATIONS]
            total_space_violations += segment_encounters[Statistics.TOTAL_SPACE_VIOLATIONS]

        return {
            Statistics.PATH_VIOLATIONS: path_violations,
            Statistics.SPACE_VIOLATIONS: space_violations,
            Statistics.TOTAL_PATH_VIOLATIONS: total_path_violations,
            Statistics.TOTAL_SPACE_VIOLATIONS: total_space_violations,
        }

    def path_segment_violations(self, path_agent: "PathAgent", path_segment: "PathSegment"):
        """
        Tracks all violations for the given path-segment.
        :param path_agent:
        :param path_segment:
        :return:
        """
        path_violations: Dict["PathAgent", List["Coordinate4D"]] = {}
        space_violations: Dict["SpaceAgent", List["Coordinate4D"]] = {}
        total_path_violations: int = 0
        total_space_violations: int = 0

        for coordinate in path_segment.coordinates:
            intersecting_agent_hashes = self.sim.environment.intersect_path_coordinate(coordinate,
                                                                                       path_agent.near_radius)
            for intersecting_agent_hash in intersecting_agent_hashes:
                intersecting_agent = self.sim.environment.agents[intersecting_agent_hash]

                if isinstance(intersecting_agent, PathAgent):
                    encountered_agent_position = intersecting_agent.get_position_at_tick(coordinate.t)
                    distance = coordinate.inter_temporal_distance(encountered_agent_position)
                    if distance <= path_agent.near_radius:
                        if intersecting_agent not in path_violations:
                            path_violations[intersecting_agent] = []
                        path_violations[intersecting_agent].append(coordinate)
                        total_path_violations += 1

                elif isinstance(intersecting_agent, SpaceAgent):
                    if intersecting_agent not in space_violations:
                        space_violations[intersecting_agent] = []
                    space_violations[intersecting_agent].append(coordinate)
                    total_space_violations += 1

                else:
                    raise Exception(f"Invalid agent {intersecting_agent}")

        return {
            Statistics.PATH_VIOLATIONS: path_violations,
            Statistics.SPACE_VIOLATIONS: space_violations,
            Statistics.TOTAL_PATH_VIOLATIONS: total_path_violations,
            Statistics.TOTAL_SPACE_VIOLATIONS: total_space_violations,
        }

    def space_segment_violations(self, space_segment: "SpaceSegment"):
        """
        Tracks all violations for the given space-segment.
        :param space_segment:
        :return:
        """
        path_violations: Dict["PathAgent", List["Coordinate4D"]] = {}
        space_violations: Dict["SpaceAgent", List["Coordinate4D"]] = {}
        total_path_violations: int = 0
        total_space_violations: int = 0

        intersecting_space_segments, intersecting_path_segments = self.sim.environment.intersect_space_segment(
            space_segment)

        for intersecting_space_agent in intersecting_space_segments:
            space_violations[intersecting_space_agent] = []
            for intersecting_space_segment in intersecting_space_segments[intersecting_space_agent]:
                space_violations[intersecting_space_agent].append(
                    space_segment.intersect(intersecting_space_segment))
                total_space_violations += 1

        for intersecting_path_agent in intersecting_path_segments:
            path_violations[intersecting_path_agent] = []
            for intersecting_path_segment in intersecting_path_segments[intersecting_path_agent]:
                for path_coordinate in intersecting_path_segment.coordinates:
                    if space_segment.contains(path_coordinate):
                        path_violations[intersecting_path_agent].append(path_coordinate)
                        total_path_violations += 1

        return {
            Statistics.PATH_VIOLATIONS: path_violations,
            Statistics.SPACE_VIOLATIONS: space_violations,
            Statistics.TOTAL_PATH_VIOLATIONS: total_path_violations,
            Statistics.TOTAL_SPACE_VIOLATIONS: total_space_violations,
        }
