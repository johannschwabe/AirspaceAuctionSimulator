import statistics
from abc import ABC
from typing import TYPE_CHECKING, List, Dict, Optional, Any

from rtree import index, Index

from .Stringify import Stringify
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

    def __init__(self, simulation: "Simulator"):
        """
        Simulation instance.
        :param simulation:
        """
        self.simulation: "Simulator" = simulation
        # Assert simulation is done
        assert simulation.time_step == simulation.environment.dimension.t + 1

        self.non_colliding_values: Dict["Agent", float] = {}
        self.values: Dict[Agent, float] = {}
        self.violations: Dict[Agent, ViolationStatistics] = {}

    def build_statistics(self) -> "SimulationStatistics":
        return SimulationStatistics(self.get_owner_statistics(),
                                    len(self.simulation.owners),
                                    len(self.simulation.environment.agents),
                                    self.get_total_value(),
                                    self.get_total_non_colliding_value(),
                                    self.get_total_violations(),
                                    self.simulation.history.total_reallocations,
                                    self.simulation.history.compute_times)

    def get_owner_statistics(self) -> List["OwnerStatistics"]:
        owner_statistics: List["OwnerStatistics"] = []
        for owner in self.simulation.owners:
            agent_statistics: List["AgentStatistics"] = []
            for agent in owner.agents:
                agent_value = self.get_value_for_agent(agent)
                non_colliding_agent_value = self.get_non_colliding_value_for_agent(agent)
                violations = self.get_agent_violations(agent)
                total_reallocations: int = self.simulation.history.reallocations[agent]
                if isinstance(agent, PathAgent):
                    path_statistics = self.path_statistics(agent.allocated_segments)
                    agent_statistics.append(PathAgentStatistics(
                        agent,
                        agent_value,
                        non_colliding_agent_value,
                        violations,
                        total_reallocations,
                        path_statistics,
                        self.get_allocation_statistics_for_agent(agent),
                    ))

                elif isinstance(agent, SpaceAgent):
                    space_statistics = self.spaces_statistics(agent.allocated_segments)
                    agent_statistics.append(SpaceAgentStatistics(
                        agent,
                        agent_value,
                        non_colliding_agent_value,
                        violations,
                        total_reallocations,
                        space_statistics,
                    ))

                else:
                    raise Exception(f"Invalid Agent: {agent}")

            owner_statistics.append(OwnerStatistics(owner,
                                                    agent_statistics,
                                                    self.get_values_for_owner(owner),
                                                    self.get_non_colliding_values_for_owner(owner)))

        return owner_statistics

    def get_allocation_statistics_for_agent(self, path_agent: "PathAgent") -> List["AllocationStatistics"]:
        allocation_statistics: List["AllocationStatistics"] = []
        for tick, allocation in self.simulation.history.allocations[path_agent].items():
            path_statistics = self.path_statistics(allocation.segments)

            colliding_agent_bids = {}
            for key, value in allocation.history.colliding_agent_bids.items():
                colliding_agent_bids[key] = value.to_dict()

            displacing_agent_bids = {}
            for key, value in allocation.history.displacing_agent_bids.items():
                displacing_agent_bids[key] = value.to_dict()

            allocation_statistics.append(AllocationStatistics(tick,
                                                              path_agent.value_for_segments(allocation.segments),
                                                              allocation.history.bid.to_dict(),
                                                              allocation.history.compute_time,
                                                              allocation.history.reason,
                                                              allocation.history.explanation,
                                                              colliding_agent_bids,
                                                              displacing_agent_bids,
                                                              path_statistics))
        return allocation_statistics

    def get_non_colliding_value_for_agent(self, agent: "Agent") -> float:
        """
        Calculate the value for an allocation on an empty map (no other agents).
        :param agent:
        :return:
        """
        if agent not in self.non_colliding_values:
            local_agent = agent.initialize_clone()
            local_env = self.simulation.environment.new_clear()
            allocation = self.simulation.mechanism.do([local_agent], local_env, 0)[local_agent]
            self.non_colliding_values[agent] = local_agent.value_for_segments(allocation.segments)
        return self.non_colliding_values[agent]

    def get_value_for_agent(self, agent: "Agent") -> float:
        """
        Calculate the value for the allocated segments of an agent.
        :param agent:
        :return:
        """
        if agent not in self.values:
            self.values[agent] = agent.get_allocated_value()
        return self.values[agent]

    def get_total_non_colliding_value(self) -> float:
        """
        Calculate the value for the allocations of all agents on an empty map summed up.
        :return:
        """
        total_value = 0
        for agent in self.simulation.environment.agents.values():
            total_value += self.get_non_colliding_value_for_agent(agent)
        return total_value

    def get_total_value(self) -> float:
        """
        Calculate the value for the allocations of all agents summed up.
        :return:
        """
        total_value = 0
        for agent in self.simulation.environment.agents.values():
            total_value += self.get_value_for_agent(agent)
        return total_value

    @staticmethod
    def _get_value_statistics(values: List[float]) -> "ValueStatistics":
        """
        Calculate statistics for a list of values
        :param values:
        :return:
        """
        total_value: int = sum(values)
        mean_value: float = statistics.mean(values)
        median_value: float = statistics.median(values)
        max_value: float = max(values)
        min_value: float = min(values)
        value_quartiles: List[float] = []
        value_outliers: List[float] = []
        if len(values) > 1:
            value_quartiles = statistics.quantiles(values)
            value_outliers = [value for value in values if
                              value < value_quartiles[0] or value > value_quartiles[-1]]
        return ValueStatistics(values,
                               total_value,
                               mean_value,
                               median_value,
                               max_value,
                               min_value,
                               value_quartiles,
                               value_outliers)

    def get_non_colliding_values_for_owner(self, owner: "Owner") -> "ValueStatistics":
        """
        Calculate the value for the allocations of all agents of an owner on an empty map summed up.
        :param owner:
        :return:
        """
        values = [self.get_non_colliding_value_for_agent(agent) for agent in owner.agents]
        return self._get_value_statistics(values)

    def get_values_for_owner(self, owner: "Owner") -> "ValueStatistics":
        """
        Calculate the value for the allocations of all agents of an owner summed up.
        :param owner:
        :return:
        """
        values = [self.get_value_for_agent(agent) for agent in owner.agents]
        return self._get_value_statistics(values)

    @staticmethod
    def path_segment_statistics(path_segment: "PathSegment") -> "PathStatistics":
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

        return PathStatistics(l1_distance,
                              l2_distance,
                              l1_ground_distance,
                              l2_ground_distance,
                              height_difference,
                              time_difference,
                              ascent,
                              descent,
                              distance_traveled,
                              ground_distance_traveled,
                              mean_height,
                              median_height,
                              heights)

    @staticmethod
    def path_statistics(path: List["PathSegment"]) -> Optional["PathStatistics"]:
        """
        Create statistics for a path (list of path-segments).
        :param path:
        :return:
        """
        if len(path) == 0:
            return None

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
            heights.extend(path_segment_statistics.heights)
            ascent += path_segment_statistics.ascent
            descent += path_segment_statistics.descent
            distance_traveled += path_segment_statistics.distance_traveled
            ground_distance_traveled += path_segment_statistics.ground_distance_traveled

        mean_height: float = statistics.mean(heights)
        median_height: int = statistics.median(heights)

        return PathStatistics(l1_distance,
                              l2_distance,
                              l1_ground_distance,
                              l2_ground_distance,
                              height_difference,
                              time_difference,
                              ascent,
                              descent,
                              distance_traveled,
                              ground_distance_traveled,
                              mean_height,
                              median_height,
                              heights)

    @staticmethod
    def space_segment_statistics(space_segment: "SpaceSegment") -> "SpaceSegmentStatistics":
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

        return SpaceSegmentStatistics(volume,
                                      height,
                                      area,
                                      time,
                                      height_above_ground)

    @staticmethod
    def _setup_rtree() -> Index:
        """
        Returns a rtree instance with 4 dimensions.
        """
        props = index.Property()
        props.dimension = 4
        return index.Rtree(properties=props)

    @staticmethod
    def spaces_statistics(spaces: List["SpaceSegment"]) -> Optional["SpaceStatistics"]:
        """
        Create statistics for spaces (list of space-segments).
        :param spaces:
        :return:
        """
        if len(spaces) == 0:
            return None

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
                intersecting_space: "Coordinate4D" = space_segment.intersect(intersecting_space_segment)
                intersecting_volume += intersecting_space.volume
                intersecting_area += intersecting_space.area

            tree.insert(hash(space_segment), space_segment.tree_rep(), obj=space_segment)

            space_segment_statistics = Statistics.space_segment_statistics(space_segment)
            summed_volume += space_segment_statistics.volume
            volumes.append(space_segment_statistics.volume)
            summed_area += space_segment_statistics.area
            areas.append(space_segment_statistics.area)
            heights.append(space_segment_statistics.height)
            times.append(space_segment_statistics.time)
            heights_above_ground.append(space_segment_statistics.height_above_ground)

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

        return SpaceStatistics(volume,
                               mean_volume,
                               median_volume,
                               mean_height,
                               median_height,
                               area,
                               mean_area,
                               median_area,
                               mean_time,
                               median_time,
                               mean_height_above_ground,
                               median_height_above_ground)

    def get_agent_violations(self, agent: "Agent") -> "ViolationStatistics":
        """
        Tracks all violations for the given agent.
        :param agent:
        :return:
        """
        if agent not in self.violations:

            violations: Dict[str, List["Coordinate4D"]] = {}
            total_violations: int = 0

            if isinstance(agent, PathAgent):
                for segment in agent.allocated_segments:
                    segment_violations = self.path_segment_violations(agent, segment)
                    violations.update(segment_violations.violations)
                    total_violations += segment_violations.total_violations

            elif isinstance(agent, SpaceAgent):
                for segment in agent.allocated_segments:
                    segment_violations = self.space_segment_violations(agent, segment)
                    violations.update(segment_violations.violations)
                    total_violations += segment_violations.total_violations

            else:
                raise Exception(f"Invalid Agent: {agent}")

            agent_violations = ViolationStatistics(violations, total_violations)
            self.violations[agent] = agent_violations

        return self.violations[agent]

    def path_segment_violations(self, path_agent: "PathAgent", path_segment: "PathSegment") -> "ViolationStatistics":
        """
        Tracks all violations for the given path-segment.
        :param path_agent:
        :param path_segment:
        :return:
        """
        violations: Dict[str, List["Coordinate4D"]] = {}
        total_violations: int = 0

        for coordinate in path_segment.coordinates:
            intersecting_agents = self.simulation.environment.intersect_path_coordinate(coordinate,
                                                                                        path_agent,
                                                                                        include_speed=False,
                                                                                        use_max_radius=False)
            for intersecting_agent in intersecting_agents:
                if isinstance(intersecting_agent, PathAgent):
                    encountered_agent_position = intersecting_agent.get_position_at_tick(coordinate.t)
                    distance = coordinate.inter_temporal_distance(encountered_agent_position, l2=True)
                    if distance <= path_agent.near_radius:
                        if intersecting_agent.id not in violations:
                            violations[intersecting_agent.id] = []
                        violations[intersecting_agent.id].append(coordinate)
                        total_violations += 1

                elif isinstance(intersecting_agent, SpaceAgent):
                    if intersecting_agent not in violations:
                        violations[intersecting_agent.id] = []
                    violations[intersecting_agent.id].append(coordinate)
                    total_violations += 1

                else:
                    raise Exception(f"Invalid agent {intersecting_agent}")

        return ViolationStatistics(violations, total_violations)

    def space_segment_violations(self, space_agent: "SpaceAgent",
                                 space_segment: "SpaceSegment") -> "ViolationStatistics":
        """
        Tracks all violations for the given space-segment.
        :param space_agent:
        :param space_segment:
        :return:
        """
        violations: Dict[str, List["Coordinate4D"]] = {}
        total_violations: int = 0

        intersecting_agents = self.simulation.environment.intersect_space_segment(
            space_segment, space_agent)

        for intersecting_agent in intersecting_agents:
            if intersecting_agent.id not in violations:
                violations[intersecting_agent.id] = []
            for space_coordinate in space_segment.coordinates:
                for intersecting_segment in intersecting_agent.allocated_segments:
                    if intersecting_segment.contains(space_coordinate):
                        violations[intersecting_agent.id].append(space_coordinate)
                        total_violations += 1

        return ViolationStatistics(violations, total_violations)

    def get_total_violations(self) -> int:
        total_violations: int = 0
        for agent in self.simulation.environment.agents.values():
            total_violations += self.get_agent_violations(agent).total_violations
        return total_violations


class PathStatistics(Stringify):
    def __init__(self,
                 l1_distance: int,
                 l2_distance: float,
                 l1_ground_distance: int,
                 l2_ground_distance: float,
                 height_difference: int,
                 time_difference: int,
                 ascent: int,
                 descent: int,
                 distance_traveled: int,
                 ground_distance_traveled: int,
                 mean_height: float,
                 median_height: int,
                 heights: List[int]):
        self.l1_distance: int = l1_distance
        self.l2_distance: float = l2_distance
        self.l1_ground_distance: int = l1_ground_distance
        self.l2_ground_distance: float = l2_ground_distance
        self.height_difference: int = height_difference
        self.time_difference: int = time_difference
        self.ascent: int = ascent
        self.descent: int = descent
        self.distance_traveled: int = distance_traveled
        self.ground_distance_traveled: int = ground_distance_traveled
        self.mean_height: float = mean_height
        self.median_height: int = median_height
        self.heights: List[int] = heights


class SpaceSegmentStatistics(Stringify):
    def __init__(self,
                 volume: int,
                 height: int,
                 area: int,
                 time: int,
                 height_above_ground: int):
        self.volume: int = volume
        self.height: int = height
        self.area: int = area
        self.time: int = time
        self.height_above_ground: int = height_above_ground


class SpaceStatistics(Stringify):
    def __init__(self,
                 volume: int,
                 mean_volume: float,
                 median_volume: int,
                 mean_height: float,
                 median_height: int,
                 area: int,
                 mean_area: float,
                 median_area: int,
                 mean_time: float,
                 median_time: int,
                 mean_height_above_ground: float,
                 median_height_above_ground: int):
        self.volume: int = volume
        self.mean_volume: float = mean_volume
        self.median_volume: int = median_volume
        self.mean_height: float = mean_height
        self.median_height: int = median_height
        self.area: int = area
        self.mean_area: float = mean_area
        self.median_area: int = median_area
        self.mean_time: float = mean_time
        self.median_time: int = median_time
        self.mean_height_above_ground: float = mean_height_above_ground
        self.median_height_above_ground: int = median_height_above_ground


class SimulationStatistics(Stringify):
    def __init__(self,
                 owners: List["OwnerStatistics"],
                 nr_owners: int,
                 nr_agents: int,
                 value: float,
                 non_colliding_value: float,
                 nr_violations: int,
                 nr_reallocations: int,
                 step_compute_time: Dict[int, int]):
        self.owners = owners
        self.total_number_of_owners = nr_owners
        self.total_number_of_agents = nr_agents
        self.total_value = value
        self.total_non_colliding_value = non_colliding_value
        self.total_number_of_violations = nr_violations
        self.total_number_of_reallocations = nr_reallocations
        self.step_compute_time: Dict[int, int] = step_compute_time


class ValueStatistics(Stringify):
    def __init__(self,
                 values: List[float],
                 total: float,
                 mean: float,
                 median: float,
                 max_value: float,
                 min_value: float,
                 quartiles: List[float],
                 outliers: List[float]):
        self.values: List[float] = values
        self.total: float = total
        self.mean: float = mean
        self.median: float = median
        self.max: float = max_value
        self.min: float = min_value
        self.quartiles: List[float] = quartiles
        self.outliers: List[float] = outliers


class OwnerStatistics(Stringify):
    def __init__(self,
                 owner: "Owner",
                 agent_statistics: List["AgentStatistics"],
                 value_statistics: ValueStatistics,
                 non_colliding_value_statistics: ValueStatistics):
        self.id: str = owner.id
        self.agents = agent_statistics
        self.total_time_in_air: int = sum(
            [agent.time_in_air if isinstance(agent, PathAgentStatistics) else 0 for agent in self.agents])
        self.values = value_statistics
        self.non_colliding_values = non_colliding_value_statistics
        self.number_of_agents: int = len(self.agents)


class AgentStatistics(ABC):
    def __init__(self,
                 agent: "Agent",
                 value: float,
                 non_colliding_value: float,
                 violation_statistics: "ViolationStatistics",
                 total_reallocations: int):
        self.id: str = agent.id
        self.value: float = value
        self.non_colliding_value: float = non_colliding_value
        self.violations = violation_statistics
        self.total_reallocations = total_reallocations


class SpaceAgentStatistics(AgentStatistics, Stringify):
    def __init__(self,
                 space_agent: "SpaceAgent",
                 value: float,
                 non_colliding_value: float,
                 violation_statistics: "ViolationStatistics",
                 total_reallocations: int,
                 space_statistics: Optional["SpaceStatistics"]):
        super().__init__(space_agent, value, non_colliding_value, violation_statistics, total_reallocations)
        self.space: Optional["SpaceStatistics"] = space_statistics


class PathAgentStatistics(AgentStatistics, Stringify):
    def __init__(self,
                 path_agent: "PathAgent",
                 value: float,
                 non_colliding_value: float,
                 violation_statistics: "ViolationStatistics",
                 total_reallocations: int,
                 path_statistics: Optional["PathStatistics"],
                 allocation_statistics: List["AllocationStatistics"]):
        super().__init__(path_agent, value, non_colliding_value, violation_statistics, total_reallocations)
        self.path: Optional["PathStatistics"] = path_statistics
        self.time_in_air: int = path_agent.get_airtime()
        self.allocations: List["AllocationStatistics"] = allocation_statistics


class AllocationStatistics(Stringify):
    def __init__(self,
                 tick: int,
                 value: float,
                 bid: Dict[str, str | int | float],
                 compute_time: int,
                 reason: str,
                 explanation: str,
                 colliding_agent_bids: Optional[Dict[str, Dict[str, str | int | float]]],
                 displacing_agent_bids: Optional[Dict[str, Dict[str, str | int | float]]],
                 path_statistics: Optional["PathStatistics"]):
        self.tick: int = tick
        self.value: float = value
        self.bid: Dict[str, str | int | float] = bid
        self.reason: str = reason
        self.explanation: str = explanation
        self.colliding_agent_bids: Dict[
            str, Dict[str, str | int | float]] = colliding_agent_bids if colliding_agent_bids is not None else {}
        self.displacing_agent_bids: Dict[
            str, Dict[str, str | int | float]] = displacing_agent_bids if displacing_agent_bids is not None else {}
        self.compute_time: int = compute_time
        self.path: Optional["PathStatistics"] = path_statistics


class ViolationStatistics(Stringify):
    def __init__(self,
                 violations: Dict[str, List["Coordinate4D"]],
                 total_violations: int):
        self.violations: Dict[str, List["Coordinate4D"]] = violations
        self.total_violations: int = total_violations


def get_statistics_dict(simulation: "Simulator") -> Dict[str, Any]:
    stats: "Statistics" = Statistics(simulation)
    return stats.build_statistics().as_dict()
