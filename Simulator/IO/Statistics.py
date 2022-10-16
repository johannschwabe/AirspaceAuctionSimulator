import statistics
from abc import ABC
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Tuple, Union, cast

from .Stringify import Stringify
from ..Agents.PathAgent import PathAgent
from ..Agents.SpaceAgent import SpaceAgent
from ..Coordinates.Coordinate2D import Coordinate2D
from ..Owners.Owner import Owner
from ..Owners.PathOwner import PathOwner
from ..Owners.SpaceOwner import SpaceOwner
from ..Segments.PathSegment import PathSegment
from ..Segments.SpaceSegment import SpaceSegment
from ..helpers.helpers import setup_rtree

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
        self.non_colliding_utilities: Dict["Agent", float] = {}
        self.values: Dict[Agent, float] = {}
        self.violations: Dict[Agent, ViolationStatistics] = {}
        self.payments = self.simulation.mechanism.calculate_final_payments(self.simulation.environment)

    def build_statistics(self) -> "SimulationStatistics":
        path_owner_stats, space_owner_stats = self.get_owner_statistics()
        owner_payments = self._get_finance_statistics(
            [stats.payments.total for stats in path_owner_stats + space_owner_stats])
        owner_utilities = self._get_finance_statistics(
            [stats.utilities.total for stats in path_owner_stats + space_owner_stats])
        owner_values = self._get_finance_statistics(
            [stats.values.total for stats in path_owner_stats + space_owner_stats])
        non_colliding_value, non_colliding_utility = self.get_total_non_colliding_outcomes()
        return SimulationStatistics(path_owner_stats, space_owner_stats,
                                    len(self.simulation.owners),
                                    len(self.simulation.environment.agents),
                                    owner_values,
                                    owner_payments,
                                    owner_utilities,
                                    non_colliding_value,
                                    non_colliding_utility,
                                    self.get_total_violations(),
                                    self.simulation.history.total_reallocations,
                                    self.simulation.history.compute_times)

    @staticmethod
    def get_path_locations_delay(path_agent: "PathAgent"):
        delayed_arrivals = []
        for _index, target in enumerate(path_agent.locations[1:]):
            if len(path_agent.allocated_segments) > _index:
                reached = path_agent.allocated_segments[_index]
                if reached.max.inter_temporal_equal(target):
                    delayed_arrivals.append(reached.max.t - target.t)
        delayed_starts = []
        for _index, target in enumerate(path_agent.locations[:-1]):
            if len(path_agent.allocated_segments) > _index:
                reached = path_agent.allocated_segments[_index]
                if _index == 0 or len(path_agent.stays) < _index:
                    stay = 0
                else:
                    stay = path_agent.stays[_index - 1]
                delayed_starts.append(reached.min.t - target.t - stay)
        rel_delayed_arrivals = []
        for _index in range(len(path_agent.locations) - 1):
            if _index < len(delayed_arrivals) and _index < len(delayed_starts):
                rel_delayed_arrivals.append(delayed_arrivals[_index] - delayed_starts[_index])
        return delayed_starts, delayed_arrivals, rel_delayed_arrivals

    def get_path_owner_stats(self, owner: "PathOwner") -> "OwnerStatistics":
        agent_statistics: List["PathAgentStatistics"] = []
        compute_time_aggr = 0
        nr_reallocations_caused_aggr = 0
        agent_values = []
        agent_payments = []
        agent_utilities = []
        for agent in owner.agents:
            assert isinstance(agent, PathAgent)
            agent_value = self.get_value_for_agent(agent)
            agent_payment = self.payments[hash(agent)]
            agent_utility = agent_value - agent_payment
            agent_values.append(agent_value)
            agent_payments.append(agent_payment)
            agent_utilities.append(agent_utility)
            non_colliding_agent_value, non_colliding_agent_utility = self.get_non_colliding_outcome_for_agent(agent)
            violations = self.get_agent_violations(agent)
            total_reallocations: int = self.simulation.history.reallocations[agent]
            compute_time = sum([allocation.history.compute_time for allocation in
                                self.simulation.history.allocations[agent].values()])
            compute_time_aggr += compute_time
            nr_reallocations_caused = sum([len(reallocation.history.colliding_agent_bids) for reallocation in
                                           self.simulation.history.allocations[agent].values() if
                                           reallocation.history.colliding_agent_bids])
            nr_reallocations_caused_aggr += nr_reallocations_caused
            path_statistics = self.path_statistics(agent.allocated_segments)
            battery_unused: int = agent.battery - agent.get_airtime()
            delayed_starts, delayed_arrivals, rel_delayed_arrivals = self.get_path_locations_delay(agent)
            agent_statistics.append(PathAgentStatistics(
                agent,
                agent_value,
                agent_payment,
                agent_utility,
                non_colliding_agent_value,
                non_colliding_agent_utility,
                violations,
                total_reallocations,
                path_statistics,
                self.get_allocation_statistics_for_agent(agent),
                compute_time,
                nr_reallocations_caused,
                battery_unused,
                delayed_starts,
                delayed_arrivals,
                rel_delayed_arrivals
            ))
        value_stats = self._get_finance_statistics(agent_values)
        payment_stats = self._get_finance_statistics(agent_payments)
        utility_stats = self._get_finance_statistics(agent_utilities)
        non_colliding_value_stats, non_colliding_utility_stats = self.get_non_colliding_outcomes_for_owner(owner)

        return OwnerStatistics(owner,
                               agent_statistics,
                               value_stats,
                               payment_stats,
                               utility_stats,
                               non_colliding_value_stats,
                               non_colliding_utility_stats,
                               compute_time_aggr,
                               nr_reallocations_caused_aggr)

    def get_space_owner_stats(self, owner: "SpaceOwner") -> "OwnerStatistics":
        agent_statistics: List["SpaceAgentStatistics"] = []
        compute_time_aggr = 0
        nr_reallocations_caused_aggr = 0
        agent_values = []
        agent_payments = []
        agent_utilities = []
        for agent in owner.agents:
            assert isinstance(agent, SpaceAgent)
            agent_value = self.get_value_for_agent(agent)
            agent_payment = self.payments[hash(agent)]
            agent_utility = agent_value - agent_payment
            agent_values.append(agent_value)
            agent_payments.append(agent_payment)
            agent_utilities.append(agent_utility)
            non_colliding_agent_value, non_colliding_agent_utility = self.get_non_colliding_outcome_for_agent(agent)
            violations = self.get_agent_violations(agent)
            total_reallocations: int = self.simulation.history.reallocations[agent]
            compute_time = sum([allocation.history.compute_time for allocation in
                                self.simulation.history.allocations[agent].values()])
            compute_time_aggr += compute_time
            nr_reallocations_caused = sum([len(reallocation.history.colliding_agent_bids) for reallocation in
                                           self.simulation.history.allocations[agent].values() if
                                           reallocation.history.colliding_agent_bids])
            nr_reallocations_caused_aggr += nr_reallocations_caused
            space_statistics = self.spaces_statistics(agent.allocated_segments)

            time_in_air = 0
            _iter = -1
            for segment in agent.allocated_segments:
                if _iter >= segment.max.t:
                    continue
                time_in_air += segment.max.t - max(segment.min.t, _iter)
                _iter = segment.max.t

            agent_statistics.append(SpaceAgentStatistics(
                agent,
                agent_value,
                agent_payment,
                agent_utility,
                non_colliding_agent_value,
                non_colliding_agent_utility,
                violations,
                total_reallocations,
                space_statistics,
                compute_time,
                nr_reallocations_caused,
                self.get_allocation_statistics_for_agent(agent),
                time_in_air
            ))
        value_stats = self._get_finance_statistics(agent_values)
        payment_stats = self._get_finance_statistics(agent_payments)
        utility_stats = self._get_finance_statistics(agent_utilities)
        non_colliding_value_stats, non_colliding_utility_stats = self.get_non_colliding_outcomes_for_owner(owner)
        return OwnerStatistics(owner,
                               agent_statistics,
                               value_stats,
                               payment_stats,
                               utility_stats,
                               non_colliding_value_stats,
                               non_colliding_utility_stats,
                               compute_time_aggr,
                               nr_reallocations_caused_aggr)

    def get_owner_statistics(self) -> Tuple[List["OwnerStatistics"], List["OwnerStatistics"]]:
        path_owner_statistics: List["OwnerStatistics"] = []
        space_owner_statistics: List["OwnerStatistics"] = []
        for owner in self.simulation.owners:
            if isinstance(owner, PathOwner):
                path_owner_statistics.append(self.get_path_owner_stats(owner))
            elif isinstance(owner, SpaceOwner):
                space_owner_statistics.append(self.get_space_owner_stats(owner))

        return path_owner_statistics, space_owner_statistics

    def get_allocation_statistics_for_agent(self, agent: "Agent") -> List["AllocationStatistics"]:
        allocation_statistics: List["AllocationStatistics"] = []
        for tick, allocation in self.simulation.history.allocations[agent].items():
            path_statistics, space_statistics = None, None
            if isinstance(agent, PathAgent):
                path_segments: List["PathSegment"] = cast(List["PathSegment"], allocation.segments)
                path_statistics = self.path_statistics(path_segments)
            elif isinstance(agent, SpaceAgent):
                space_segments: List["SpaceSegment"] = cast(List["SpaceSegment"], allocation.segments)
                space_statistics = self.spaces_statistics(space_segments)
            else:
                raise Exception(f"Invalid Agent: {agent}")

            colliding_agent_bids = {}
            if allocation.history.colliding_agent_bids is not None:
                for key, value in allocation.history.colliding_agent_bids.items():
                    colliding_agent_bids[key] = value.to_dict()

            displacing_agent_bids = {}
            if allocation.history.displacing_agent_bids is not None:
                for key, value in allocation.history.displacing_agent_bids.items():
                    displacing_agent_bids[key] = value.to_dict()
            value = agent.value_for_segments(allocation.segments)
            payment = allocation.preliminary_payment
            utility = value - payment
            allocation_statistics.append(AllocationStatistics(tick,
                                                              value,
                                                              payment,
                                                              utility,
                                                              allocation.history.bid.to_dict(),
                                                              allocation.history.compute_time,
                                                              allocation.history.reason,
                                                              allocation.history.explanation,
                                                              colliding_agent_bids=colliding_agent_bids,
                                                              displacing_agent_bids=displacing_agent_bids,
                                                              path_statistics=path_statistics,
                                                              space_statistics=space_statistics))
        return allocation_statistics

    def get_non_colliding_outcome_for_agent(self, agent: "Agent") -> Tuple[float, float]:
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
            local_env.agents = {hash(local_agent): local_agent}
            local_agent.allocated_segments = allocation.segments
            final_payments = self.simulation.mechanism.calculate_final_payments(local_env)
            payment = final_payments[hash(agent)] if hash(agent) in final_payments else 0
            self.non_colliding_utilities[agent] = self.non_colliding_values[
                                                      agent] - payment
        return self.non_colliding_values[agent], self.non_colliding_utilities[agent]

    def get_value_for_agent(self, agent: "Agent") -> float:
        """
        Calculate the value for the allocated segments of an agent.
        :param agent:
        :return:
        """
        if agent not in self.values:
            self.values[agent] = agent.get_allocated_value()
        return self.values[agent]

    def get_total_non_colliding_outcomes(self) -> Tuple[float, float]:
        """
        Calculate the value for the allocations of all agents on an empty map summed up.
        :return:
        """
        total_value = 0
        total_utility = 0
        for agent in self.simulation.environment.agents.values():
            agent_value, agent_utility = self.get_non_colliding_outcome_for_agent(agent)
            total_value += agent_value
            total_utility += agent_utility
        return total_value, total_utility

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
    def _get_finance_statistics(finance: List[float]) -> "FinanceStatistics":
        """
        Calculate statistics for a list of values
        :param finance:
        :return:
        """
        total_value: int = sum(finance)
        mean_value: float = statistics.mean(finance)
        median_value: float = statistics.median(finance)
        max_value: float = max(finance)
        min_value: float = min(finance)
        value_quartiles: List[float] = []
        if len(finance) == 1:
            value_quartiles = [finance[0]] * 3
        if len(finance) == 2 or len(finance) == 3:
            value_quartiles = [min_value, mean_value, max_value]
        if len(finance) > 3:
            value_quartiles = statistics.quantiles(finance)
        value_outliers = [value for value in finance if
                          value < value_quartiles[0] or value > value_quartiles[-1]]
        return FinanceStatistics(finance,
                                 total_value,
                                 mean_value,
                                 median_value,
                                 max_value,
                                 min_value,
                                 value_quartiles,
                                 value_outliers)

    def get_non_colliding_outcomes_for_owner(self, owner: "Owner") -> Tuple["FinanceStatistics", "FinanceStatistics"]:
        """
        Calculate the value for the allocations of all agents of an owner on an empty map summed up.
        :param owner:
        :return:
        """
        values = [self.get_non_colliding_outcome_for_agent(agent)[0] for agent in owner.agents]
        utilities = [self.get_non_colliding_outcome_for_agent(agent)[1] for agent in owner.agents]
        return self._get_finance_statistics(values), self._get_finance_statistics(utilities)

    @staticmethod
    def path_segment_statistics(path_segment: "PathSegment") -> "PathStatistics":
        """
        Create statistics for a path-segment.
        :param path_segment:
        :return:
        """
        delta = path_segment.max - path_segment.min

        l1_distance: float = delta.to_3D().l1
        l2_distance: float = delta.to_3D().l2
        l1_ground_distance: float = delta.to_2D().l1
        l2_ground_distance: float = delta.to_2D().l2
        height_difference: float = path_segment.max.y - path_segment.min.y
        time_difference: int = path_segment.max.t - path_segment.min.t
        heights: List[float] = []
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
        median_height: float = statistics.median(heights)

        return PathStatistics(l1_distance,
                              l2_distance,
                              l1_ground_distance,
                              l2_ground_distance,
                              height_difference,
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

        l1_distance: float = int(path[0].min.distance(path[-1].max))
        l2_distance: float = path[0].min.distance(path[-1].max, l2=True)
        l1_ground_distance: float = int(Coordinate2D.distance(path[0].min, path[-1].max))
        l2_ground_distance: float = Coordinate2D.distance(path[0].min, path[-1].max, l2=True)
        height_difference: float = path[-1].max.y - path[0].min.y
        heights: List[float] = []
        ascent: float = 0
        descent: float = 0
        distance_traveled: float = 0
        ground_distance_traveled: float = 0
        for path_segment in path:
            path_segment_statistics = Statistics.path_segment_statistics(path_segment)
            heights.extend(path_segment_statistics.heights)
            ascent += path_segment_statistics.ascent
            descent += path_segment_statistics.descent
            distance_traveled += path_segment_statistics.distance_traveled
            ground_distance_traveled += path_segment_statistics.ground_distance_traveled

        mean_height: float = statistics.mean(heights)
        median_height: float = statistics.median(heights)

        return PathStatistics(l1_distance,
                              l2_distance,
                              l1_ground_distance,
                              l2_ground_distance,
                              height_difference,
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

        tree = setup_rtree()

        for space_segment in spaces:
            intersections = tree.intersection(space_segment.tree_rep(), objects="raw")
            for intersecting_space_segment in intersections:
                assert isinstance(intersecting_space_segment, SpaceSegment)
                intersection_volume = space_segment.intersection_volume(
                    intersecting_space_segment)
                intersecting_volume += intersection_volume.volume
                intersecting_area += intersection_volume.area

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

    @staticmethod
    def merge_violations(violations: Dict[Union[str, int], List["Coordinate4D"]],
                         new_violations: Dict[Union[str, int], List["Coordinate4D"]]):
        for key, value in new_violations.items():
            if key in violations:
                violations[key].extend(value)
            else:
                violations[key] = value

    def get_agent_violations(self, agent: "Agent") -> "ViolationStatistics":
        """
        Tracks all violations for the given agent.
        :param agent:
        :return:
        """
        if agent not in self.violations:

            violations: Dict[str, List["Coordinate4D"]] = {}
            blocker_violations: Dict[int, List["Coordinate4D"]] = {}
            total_violations: int = 0
            total_blocker_violations: int = 0
            incomplete_allocation = False

            if isinstance(agent, PathAgent):
                for segment in agent.allocated_segments:
                    segment_violations = self.path_segment_violations(agent, segment)
                    self.merge_violations(violations, segment_violations.violations)
                    self.merge_violations(blocker_violations, segment_violations.blocker_violations)
                    total_violations += segment_violations.total_violations
                    total_blocker_violations += segment_violations.total_blocker_violations

                if len(agent.allocated_segments) > 0 and len(agent.allocated_segments[0].coordinates) > 0 and not \
                        agent.allocated_segments[-1].max.inter_temporal_equal(agent.locations[-1]):
                    incomplete_allocation = True
                    total_violations += 1

            elif isinstance(agent, SpaceAgent):
                for segment in agent.allocated_segments:
                    segment_violations = self.space_segment_violations(agent, segment)
                    self.merge_violations(violations, segment_violations.violations)
                    total_violations += segment_violations.total_violations

            else:
                raise Exception(f"Invalid Agent: {agent}")

            agent_violations = ViolationStatistics(violations, total_violations, blocker_violations,
                                                   total_blocker_violations, incomplete_allocation)
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
        blocker_violations: Dict[int, List["Coordinate4D"]] = {}
        total_violations: int = 0
        total_blocker_violations: int = 0

        for coordinate in path_segment.coordinates:
            intersecting_agents = self.simulation.environment.intersect_path_coordinate(coordinate,
                                                                                        path_agent,
                                                                                        include_speed=False,
                                                                                        use_max_radius=False)
            for intersecting_agent in intersecting_agents:
                true_intersection = False

                if isinstance(intersecting_agent, PathAgent):
                    encountered_agent_position = intersecting_agent.get_position_at_tick(coordinate.t)
                    assert encountered_agent_position is not None
                    distance = coordinate.distance(encountered_agent_position, l2=True)
                    if distance <= path_agent.near_radius:
                        true_intersection = True

                elif isinstance(intersecting_agent, SpaceAgent):
                    encountered_agent_segments = intersecting_agent.get_segments_at_tick(coordinate.t)
                    assert len(encountered_agent_segments) > 0
                    for segment in encountered_agent_segments:
                        distance = coordinate.distance_to_space(segment.min, segment.max)
                        if distance <= path_agent.near_radius:
                            true_intersection = True
                            break

                else:
                    raise Exception(f"Invalid agent {intersecting_agent}")

                if true_intersection:
                    if intersecting_agent.id not in violations:
                        violations[intersecting_agent.id] = []
                    violations[intersecting_agent.id].append(coordinate)
                    total_violations += 1

            blocker_intersections = self.simulation.environment.get_blockers_at_coordinate(coordinate,
                                                                                           path_agent.near_radius, 0)
            for blocker in blocker_intersections:
                if blocker.is_blocking(coordinate, path_agent.near_radius):
                    if blocker.id not in blocker_violations:
                        blocker_violations[blocker.id] = []
                    blocker_violations[blocker.id].append(coordinate)
                    total_blocker_violations += 1

        return ViolationStatistics(violations, total_violations, blocker_violations, total_blocker_violations)

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
            if isinstance(intersecting_agent, PathAgent):
                intersecting_agents_coords = intersecting_agent.get_positions_at_ticks(space_segment.min.t,
                                                                                       space_segment.max.t)
                for possible_collision in intersecting_agents_coords:
                    if space_segment.contains(possible_collision):
                        violations[intersecting_agent.id].append(possible_collision)
                        total_violations += 1

            elif isinstance(intersecting_agent, SpaceAgent):
                intersecting_agents_segments = intersecting_agent.get_segments_at_ticks(space_segment.min.t,
                                                                                        space_segment.max.t)
                for segment in intersecting_agents_segments:
                    intersecting_min, intersecting_max = segment.intersecting_space(space_segment)
                    if (intersecting_max - intersecting_min).volume > 0:
                        intersection_point = (intersecting_min + intersecting_max) / 2

                        for t in range(intersecting_max.t - intersecting_min.t):
                            violations[intersecting_agent.id].append(
                                Coordinate4D.from_3D(intersection_point, intersecting_min.t + t))
                            total_violations += 1
        return ViolationStatistics(violations, total_violations)

    def get_total_violations(self) -> int:
        total_violations: int = 0
        for agent in self.simulation.environment.agents.values():
            total_violations += self.get_agent_violations(agent).total_violations + self.get_agent_violations(
                agent).total_blocker_violations
        return total_violations


class PathStatistics(Stringify):
    def __init__(self,
                 l1_distance: float,
                 l2_distance: float,
                 l1_ground_distance: float,
                 l2_ground_distance: float,
                 height_difference: float,
                 ascent: float,
                 descent: float,
                 distance_traveled: float,
                 ground_distance_traveled: float,
                 mean_height: float,
                 median_height: float,
                 heights: List[float]):
        self.l1_distance: float = l1_distance
        self.l2_distance: float = l2_distance
        self.l1_ground_distance: float = l1_ground_distance
        self.l2_ground_distance: float = l2_ground_distance
        self.height_difference: float = height_difference
        self.ascent: float = ascent
        self.descent: float = descent
        self.distance_traveled: float = distance_traveled
        self.ground_distance_traveled: float = ground_distance_traveled
        self.mean_height: float = mean_height
        self.median_height: float = median_height
        self.heights: List[float] = heights


class SpaceSegmentStatistics(Stringify):
    def __init__(self,
                 volume: float,
                 height: float,
                 area: float,
                 time: int,
                 height_above_ground: float):
        self.volume: float = volume
        self.height: float = height
        self.area: float = area
        self.time: int = time
        self.height_above_ground: float = height_above_ground


class SpaceStatistics(Stringify):
    def __init__(self,
                 volume: float,
                 mean_volume: float,
                 median_volume: float,
                 mean_height: float,
                 median_height: float,
                 area: float,
                 mean_area: float,
                 median_area: float,
                 mean_time: float,
                 median_time: int,
                 mean_height_above_ground: float,
                 median_height_above_ground: float):
        self.volume: float = volume
        self.mean_volume: float = mean_volume
        self.median_volume: float = median_volume
        self.mean_height: float = mean_height
        self.median_height: float = median_height
        self.area: float = area
        self.mean_area: float = mean_area
        self.median_area: float = median_area
        self.mean_time: float = mean_time
        self.median_time: int = median_time
        self.mean_height_above_ground: float = mean_height_above_ground
        self.median_height_above_ground: float = median_height_above_ground


class SimulationStatistics(Stringify):
    def __init__(self,
                 path_owners: List["OwnerStatistics"],
                 space_owners: List["OwnerStatistics"],
                 nr_owners: int,
                 nr_agents: int,
                 value_stats: "FinanceStatistics",
                 payment_stats: "FinanceStatistics",
                 utility_stats: "FinanceStatistics",
                 non_colliding_value: float,
                 non_colliding_utility: float,
                 nr_violations: int,
                 nr_reallocations: int,
                 step_compute_time: Dict[int, int]):
        self.path_owners = path_owners
        self.space_owners = space_owners
        self.total_number_of_owners = nr_owners
        self.total_number_of_agents = nr_agents
        self.value_stats = value_stats
        self.payment_stats = payment_stats
        self.utility_stats = utility_stats
        self.total_non_colliding_value = non_colliding_value
        self.total_non_colliding_utility = non_colliding_utility
        self.total_number_of_violations = nr_violations
        self.total_number_of_reallocations = nr_reallocations
        self.step_compute_time: Dict[int, int] = step_compute_time


class FinanceStatistics(Stringify):
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
                 value_stats: FinanceStatistics,
                 payment_stats: FinanceStatistics,
                 utility_stats: FinanceStatistics,
                 non_colliding_value_statistics: FinanceStatistics,
                 non_colliding_utility_statistics: FinanceStatistics,
                 compute_time: int,
                 nr_reallocations_caused_aggr: int):
        self.id: str = owner.id
        self.agents = agent_statistics
        self.total_time_in_air: int = sum([agent.time_in_air for agent in self.agents])
        self.values = value_stats
        self.payments = payment_stats
        self.utilities = utility_stats
        self.non_colliding_values = non_colliding_value_statistics
        self.non_colliding_utility = non_colliding_utility_statistics
        self.number_of_agents: int = len(self.agents)
        self.compute_time = compute_time
        self.nr_reallocations_caused = nr_reallocations_caused_aggr
        self.nr_battery_overused = sum([agent_statistic.battery_unused < 0 for agent_statistic in agent_statistics if
                                        isinstance(agent_statistic, PathAgentStatistics)])


class AgentStatistics(ABC):
    def __init__(self,
                 agent: "Agent",
                 value: float,
                 payment: float,
                 utility: float,
                 non_colliding_value: float,
                 non_colliding_utility: float,
                 violation_statistics: "ViolationStatistics",
                 total_reallocations: int,
                 compute_time: int,
                 nr_reallocations_caused: int,
                 allocation_statistics: List["AllocationStatistics"],
                 time_in_air: int):
        self.id: str = agent.id
        self.value: float = value
        self.payment: float = payment
        self.utility: float = utility
        self.non_colliding_value: float = non_colliding_value
        self.non_colliding_utility: float = non_colliding_utility
        self.violations = violation_statistics
        self.total_reallocations = total_reallocations
        self.compute_time = compute_time
        self.nr_reallocations_caused = nr_reallocations_caused
        self.allocations: List["AllocationStatistics"] = allocation_statistics
        self.time_in_air: int = time_in_air


class SpaceAgentStatistics(AgentStatistics, Stringify):
    def __init__(self,
                 space_agent: "SpaceAgent",
                 value: float,
                 payment: float,
                 utility: float,
                 non_colliding_value: float,
                 non_colliding_utility: float,
                 violation_statistics: "ViolationStatistics",
                 total_reallocations: int,
                 space_statistics: Optional["SpaceStatistics"],
                 compute_time: int,
                 nr_reallocations_caused: int,
                 allocation_statistics: List["AllocationStatistics"],
                 time_in_air: int
                 ):
        super().__init__(space_agent, value, payment, utility, non_colliding_value, non_colliding_utility,
                         violation_statistics, total_reallocations, compute_time, nr_reallocations_caused,
                         allocation_statistics, time_in_air)
        self.space: Optional["SpaceStatistics"] = space_statistics


class PathAgentStatistics(AgentStatistics, Stringify):
    def __init__(self,
                 path_agent: "PathAgent",
                 value: float,
                 payment: float,
                 utility: float,
                 non_colliding_value: float,
                 non_colliding_utility: float,
                 violation_statistics: "ViolationStatistics",
                 total_reallocations: int,
                 path_statistics: Optional["PathStatistics"],
                 allocation_statistics: List["AllocationStatistics"],
                 compute_time: int,
                 nr_reallocations_caused: int,
                 battery_unused: int,
                 delayed_starts: List[int],
                 delayed_arrivals: List[int],
                 re_delayed_arrivals: List[int]):
        super().__init__(path_agent, value, payment, utility, non_colliding_value, non_colliding_utility,
                         violation_statistics,
                         total_reallocations,
                         compute_time, nr_reallocations_caused, allocation_statistics, path_agent.get_airtime())
        self.path: Optional["PathStatistics"] = path_statistics
        self.battery_unused: int = battery_unused
        self.delayed_starts = delayed_starts
        self.delayed_arrivals = delayed_arrivals
        self.re_delayed_arrivals = re_delayed_arrivals


class AllocationStatistics(Stringify):
    def __init__(self,
                 tick: int,
                 value: float,
                 payment: float,
                 utility: float,
                 bid: Dict[str, Union[str, int, float]],
                 compute_time: int,
                 reason: str,
                 explanation: str,
                 colliding_agent_bids: Optional[Dict[str, Dict[str, Union[str, int, float]]]],
                 displacing_agent_bids: Optional[Dict[str, Dict[str, Union[str, int, float]]]],
                 path_statistics: Optional["PathStatistics"],
                 space_statistics: Optional["SpaceStatistics"]):
        self.tick: int = tick
        self.value: float = value
        self.payment: float = payment
        self.utility: float = utility
        self.bid: Dict[str, Union[str, int, float]] = bid
        self.reason: str = reason
        self.explanation: str = explanation
        self.colliding_agent_bids: Dict[
            str, Dict[str, Union[str, int, float]]] = colliding_agent_bids if colliding_agent_bids is not None else {}
        self.displacing_agent_bids: Dict[
            str, Dict[str, Union[str, int, float]]] = displacing_agent_bids if displacing_agent_bids is not None else {}
        self.compute_time: int = compute_time
        self.path: Optional["PathStatistics"] = path_statistics
        self.space: Optional["SpaceStatistics"] = space_statistics


class ViolationStatistics(Stringify):
    def __init__(self,
                 violations: Dict[str, List["Coordinate4D"]],
                 total_violations: int,
                 blocker_violations: Optional[Dict[int, List["Coordinate4D"]]] = None,
                 total_blocker_violations: Optional[int] = 0,
                 incomplete_allocation: bool = False):
        self.violations: Dict[str, List["Coordinate4D"]] = violations
        self.total_violations: int = total_violations
        self.blocker_violations: Optional[Dict[int, List["Coordinate4D"]]] = blocker_violations
        self.total_blocker_violations: int = total_blocker_violations
        self.incomplete_allocation: bool = incomplete_allocation


def get_statistics_dict(simulation: "Simulator") -> Dict[str, Any]:
    stats: "Statistics" = Statistics(simulation)
    return stats.build_statistics().as_dict()
