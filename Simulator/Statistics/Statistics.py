import statistics
from typing import TYPE_CHECKING, List, Dict, Optional

from ..Agents.PathAgent import PathAgent
from ..Agents.SpaceAgent import SpaceAgent
from ..Coordinates.Coordinate2D import Coordinate2D
from ..Coordinates.Coordinate3D import Coordinate3D
from ..Owners.Owner import Owner
from ..Segments.PathSegment import PathSegment

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Simulator import Simulator
    from ..Agents.Agent import Agent


class Statistics:
    """
    Statistics class that generates statistics for a simulation.
    """
    # Path Statistics
    L1_DISTANCE = "l1_distance"
    L2_DISTANCE = "l2_distance"
    L1_GROUND_DISTANCE = "l1_ground_distance"
    L2_GROUND_DISTANCE = "l2_ground_distance"
    HEIGHT_DIFFERENCE = "height_difference"
    TIME_DIFFERENCE = "time_difference"
    ASCENT = "ascent"
    DESCENT = "descent"
    L1_DISTANCE_TRAVELED = "l1_distance_traveled"
    L2_DISTANCE_TRAVELED = "l2_distance_traveled"
    L1_GROUND_DISTANCE_TRAVELED = "l1_ground_distance_traveled"
    L2_GROUND_DISTANCE_TRAVELED = "l2_ground_distance_traveled"
    MEAN_HEIGHT = "mean_height"
    MEDIAN_HEIGHT = "median_height"
    DELTAS = "deltas"
    HEIGHTS = "heights"

    # Path Encounters
    ENCOUNTERS = "encounters"
    INCOMING_VIOLATIONS = "incoming_violations"
    OUTGOING_VIOLATIONS = "outgoing_violations"
    SPACE_VIOLATIONS = "space_violations"
    TOTAL_ENCOUNTERS = "total_encounters"
    TOTAL_INCOMING_VIOLATIONS = "total_incoming_violations"
    TOTAL_OUTGOING_VIOLATIONS = "total_outgoing_violations"
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
        l1_distance: int = int(path_segment.min.inter_temporal_distance(path_segment.max))
        l2_distance: float = path_segment.min.inter_temporal_distance(path_segment.max, l2=True)
        l1_ground_distance: int = int(Coordinate2D.distance(path_segment.min, path_segment.max))
        l2_ground_distance: float = Coordinate2D.distance(path_segment.min, path_segment.max, l2=True)
        height_difference: int = path_segment.max.y - path_segment.min.y
        time_difference: int = path_segment.max.t - path_segment.min.t
        heights: List[int] = []
        deltas: List["Coordinate3D"] = []
        ascent: int = 0
        descent: int = 0
        l1_distance_traveled: int = 0
        l2_distance_traveled: int = 0
        l1_ground_distance_traveled: int = 0
        l2_ground_distance_traveled: int = 0
        previous_coordinate: Optional["Coordinate4D"] = None
        for coordinate in path_segment.coordinates:
            if previous_coordinate is not None:
                # height
                delta_y = coordinate.y - previous_coordinate.y
                if delta_y > 0:
                    ascent += delta_y
                elif delta_y < 0:
                    descent += abs(delta_y)
                # distance
                delta = previous_coordinate - coordinate
                deltas.append(delta)
                l1_distance_traveled += delta.l1
                l2_distance_traveled += delta.l2
                l1_ground_distance_traveled += Coordinate2D.distance(previous_coordinate, coordinate)
                l2_ground_distance_traveled += Coordinate2D.distance(previous_coordinate, coordinate, l2=True)
            # heights
            heights.append(coordinate.y)
            # update previous for loop
            previous_coordinate = coordinate

        mean_height: float = statistics.mean(heights)
        median_height: int = statistics.median(heights)

        return {
            Statistics.L1_DISTANCE: l1_distance,
            Statistics.L2_DISTANCE: l2_distance,
            Statistics.L1_GROUND_DISTANCE: l1_ground_distance,
            Statistics.L2_GROUND_DISTANCE: l2_ground_distance,
            Statistics.HEIGHT_DIFFERENCE: height_difference,
            Statistics.TIME_DIFFERENCE: time_difference,
            Statistics.ASCENT: ascent,
            Statistics.DESCENT: descent,
            Statistics.L1_DISTANCE_TRAVELED: l1_distance_traveled,
            Statistics.L2_DISTANCE_TRAVELED: l2_distance_traveled,
            Statistics.L1_GROUND_DISTANCE_TRAVELED: l1_ground_distance_traveled,
            Statistics.L2_GROUND_DISTANCE_TRAVELED: l2_ground_distance_traveled,
            Statistics.MEAN_HEIGHT: mean_height,
            Statistics.MEDIAN_HEIGHT: median_height,
            Statistics.DELTAS: deltas,
            Statistics.HEIGHTS: heights,
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
        deltas: List["Coordinate3D"] = []
        ascent: int = 0
        descent: int = 0
        l1_distance_traveled: int = 0
        l2_distance_traveled: int = 0
        l1_ground_distance_traveled: int = 0
        l2_ground_distance_traveled: int = 0
        for path_segment in path:
            path_segment_statistics = Statistics.path_segment_statistics(path_segment)
            heights.extend(path_segment_statistics[Statistics.HEIGHTS])
            deltas.extend(path_segment_statistics[Statistics.DELTAS])
            ascent += path_segment_statistics[Statistics.ASCENT]
            descent += path_segment_statistics[Statistics.DESCENT]
            l1_distance_traveled += path_segment_statistics[Statistics.L1_DISTANCE_TRAVELED]
            l2_distance_traveled += path_segment_statistics[Statistics.L2_DISTANCE_TRAVELED]
            l1_ground_distance_traveled += path_segment_statistics[Statistics.L1_GROUND_DISTANCE_TRAVELED]
            l2_ground_distance_traveled += path_segment_statistics[Statistics.L2_GROUND_DISTANCE_TRAVELED]

        mean_height: float = statistics.mean(heights)
        median_height: int = statistics.median(heights)

        return {
            Statistics.L1_DISTANCE: l1_distance,
            Statistics.L2_DISTANCE: l2_distance,
            Statistics.L1_GROUND_DISTANCE: l1_ground_distance,
            Statistics.L2_GROUND_DISTANCE: l2_ground_distance,
            Statistics.HEIGHT_DIFFERENCE: height_difference,
            Statistics.TIME_DIFFERENCE: time_difference,
            Statistics.ASCENT: ascent,
            Statistics.DESCENT: descent,
            Statistics.L1_DISTANCE_TRAVELED: l1_distance_traveled,
            Statistics.L2_DISTANCE_TRAVELED: l2_distance_traveled,
            Statistics.L1_GROUND_DISTANCE_TRAVELED: l1_ground_distance_traveled,
            Statistics.L2_GROUND_DISTANCE_TRAVELED: l2_ground_distance_traveled,
            Statistics.MEAN_HEIGHT: mean_height,
            Statistics.MEDIAN_HEIGHT: median_height,
            Statistics.DELTAS: deltas,
            Statistics.HEIGHTS: heights,
        }

    def path_segment_encounters(self, path_agent: "PathAgent", path_segment: "PathSegment"):
        """
        Tracks all encounters and violation for the given path-segment.
        :param path_agent:
        :param path_segment:
        :return:
        """
        encounters: Dict["Coordinate4D", List["PathAgent"]] = {}
        incoming_violations: Dict["Coordinate4D", List["PathAgent"]] = {}
        outgoing_violations: Dict["Coordinate4D", List["PathAgent"]] = {}
        space_violations: Dict["Coordinate4D", List["SpaceAgent"]] = {}
        total_encounters: int = 0
        total_incoming_violations: int = 0
        total_outgoing_violations: int = 0
        total_space_violations: int = 0

        for coordinate in path_segment.coordinates:
            encountered_agents_hashes = self.sim.environment.intersect(coordinate, self.sim.environment.max_near_radius)
            for encountered_agent_hash in encountered_agents_hashes:
                encountered_agent = self.sim.environment.agents[encountered_agent_hash]

                if isinstance(encountered_agent, PathAgent):
                    encountered_agent_position = encountered_agent.get_position_at_tick(coordinate.t)
                    distance = coordinate.inter_temporal_distance(encountered_agent_position)
                    if distance <= path_agent.near_radius + encountered_agent.near_radius:
                        # add agent to encounters
                        if coordinate not in encounters:
                            encounters[coordinate] = []
                        encounters[coordinate].append(encountered_agent)
                        total_encounters += 1

                        if distance <= path_agent.near_radius:
                            # add agent to incoming violations
                            if coordinate not in incoming_violations:
                                incoming_violations[coordinate] = []
                            incoming_violations[coordinate].append(encountered_agent)
                            total_incoming_violations += 1

                        if distance <= encountered_agent.near_radius:
                            # add agent to outgoing violations
                            if coordinate not in outgoing_violations:
                                outgoing_violations[coordinate] = []
                            outgoing_violations[coordinate].append(encountered_agent)
                            total_outgoing_violations += 1

                elif isinstance(encountered_agent, SpaceAgent):
                    # add agent to space violations
                    if coordinate not in space_violations:
                        space_violations[coordinate] = []
                    space_violations[coordinate].append(encountered_agent)
                    total_space_violations += 1

        return {
            Statistics.ENCOUNTERS: encounters,
            Statistics.INCOMING_VIOLATIONS: incoming_violations,
            Statistics.OUTGOING_VIOLATIONS: outgoing_violations,
            Statistics.SPACE_VIOLATIONS: space_violations,
            Statistics.TOTAL_ENCOUNTERS: total_encounters,
            Statistics.TOTAL_INCOMING_VIOLATIONS: total_incoming_violations,
            Statistics.TOTAL_OUTGOING_VIOLATIONS: total_outgoing_violations,
            Statistics.TOTAL_SPACE_VIOLATIONS: total_space_violations,
        }

    def path_agent_encounters(self, path_agent: "PathAgent"):
        """
        Tracks all encounters and violation for the given path-agent.
        :param path_agent:
        :return:
        """
        encounters: Dict["Coordinate4D", List["PathAgent"]] = {}
        incoming_violations: Dict["Coordinate4D", List["PathAgent"]] = {}
        outgoing_violations: Dict["Coordinate4D", List["PathAgent"]] = {}
        space_violations: Dict["Coordinate4D", List["SpaceAgent"]] = {}
        total_encounters: int = 0
        total_incoming_violations: int = 0
        total_outgoing_violations: int = 0
        total_space_violations: int = 0

        for path_segment in path_agent.allocated_segments:
            path_segment_encounters = self.path_segment_encounters(path_agent, path_segment)
            encounters.update(path_segment_encounters[Statistics.ENCOUNTERS])
            incoming_violations.update(path_segment_encounters[Statistics.INCOMING_VIOLATIONS])
            outgoing_violations.update(path_segment_encounters[Statistics.OUTGOING_VIOLATIONS])
            space_violations.update(path_segment_encounters[Statistics.SPACE_VIOLATIONS])
            total_encounters += path_segment_encounters[Statistics.TOTAL_ENCOUNTERS]
            total_incoming_violations += path_segment_encounters[Statistics.TOTAL_INCOMING_VIOLATIONS]
            total_outgoing_violations += path_segment_encounters[Statistics.TOTAL_OUTGOING_VIOLATIONS]
            total_space_violations += path_segment_encounters[Statistics.TOTAL_SPACE_VIOLATIONS]

        return {
            Statistics.ENCOUNTERS: encounters,
            Statistics.INCOMING_VIOLATIONS: incoming_violations,
            Statistics.OUTGOING_VIOLATIONS: outgoing_violations,
            Statistics.SPACE_VIOLATIONS: space_violations,
            Statistics.TOTAL_ENCOUNTERS: total_encounters,
            Statistics.TOTAL_INCOMING_VIOLATIONS: total_incoming_violations,
            Statistics.TOTAL_OUTGOING_VIOLATIONS: total_outgoing_violations,
            Statistics.TOTAL_SPACE_VIOLATIONS: total_space_violations,
        }
