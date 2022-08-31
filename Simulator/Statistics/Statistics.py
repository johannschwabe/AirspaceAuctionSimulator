import statistics
from typing import TYPE_CHECKING, List, Dict, Optional

from ..Agents.PathAgent import PathAgent
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
        previous_coord: Optional["Coordinate4D"] = None
        for coord in path_segment.coordinates:
            if previous_coord is not None:
                # height
                delta_y = coord.y - previous_coord.y
                if delta_y > 0:
                    ascent += delta_y
                elif delta_y < 0:
                    descent += abs(delta_y)
                # distance
                delta = previous_coord - coord
                deltas.append(delta)
                l1_distance_traveled += delta.l1
                l2_distance_traveled += delta.l2
                l1_ground_distance_traveled += Coordinate2D.distance(previous_coord, coord)
                l2_ground_distance_traveled += Coordinate2D.distance(previous_coord, coord, l2=True)
            # heights
            heights.append(coord.y)
            # update previous for loop
            previous_coord = coord

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

    def close_encounters(self):
        """
        Detect all close encounters.
        :return:
        """
        res = {}
        near_radi = [_agent.near_radius for _agent in self.sim.environment.agents.values() if
                     isinstance(_agent, PathAgent)]
        near_radi.append(0)
        max_near_radi = max(near_radi)

        for agent in self.sim.environment.agents.values():
            res[agent.id] = {
                "near_field_violations": {},
                "near_field_intersection": {},
                "total_near_field_violations": 0,
                "total_near_field_intersection": 0,
            }
            for segment in agent.allocated_segments:
                if isinstance(segment, PathSegment) and isinstance(agent, PathAgent):
                    for step in segment.coordinates[::agent.speed]:
                        res[agent.id]["near_field_violations"][step.t] = self.violations(step, agent,
                                                                                         agent.near_radius)
                        near_intersections = \
                            self.intersections(step, agent, max_near_radi)
                        res[agent.id]["near_field_intersection"][step.t] = near_intersections
                        res[agent.id]["total_near_field_violations"] += \
                            res[agent.id]["near_field_violations"][step.t]
                        res[agent.id]["total_near_field_intersection"] += \
                            res[agent.id]["near_field_intersection"][
                                step.t]
        return res

    def violations(self, position: "Coordinate4D", agent: "PathAgent", radi: int):
        """
        Detect all violations.
        :param position:
        :param agent:
        :param radi:
        :return:
        """
        box = [position.x - radi,
               position.y - radi,
               position.z - radi,
               position.t,
               position.x + radi,
               position.y + radi,
               position.z + radi,
               position.t + agent.speed - 1]
        collisions = self.sim.environment.tree.intersection(box, objects=True)
        real_collisions = filter(lambda col: col.id != agent.id, collisions)
        count = 0
        for real_collision in real_collisions:
            start = max(real_collision.bbox[3], position.t)
            end = min(real_collision.bbox[7], position.t + agent.speed - 1)
            count += int(end) - int(start) + 1
        return count

    def intersections(self, position: "Coordinate4D", agent: "Agent", max_near_radi):
        """
        Detect all intersections.
        :param position:
        :param agent:
        :param max_near_radi:
        :return:
        """
        near_intersections = 0
        real_agent: "Agent" = self.sim.environment.agents[hash(agent)]
        if isinstance(real_agent, PathAgent):
            box = [position.x - max_near_radi,
                   position.y - max_near_radi,
                   position.z - max_near_radi,
                   position.t,
                   position.x + max_near_radi,
                   position.y + max_near_radi,
                   position.z + max_near_radi,
                   position.t + real_agent.speed]
            collisions = self.sim.environment.tree.intersection(box, objects=True)
            real_collisions = filter(lambda col: col.id != hash(agent), collisions)

            for collision in real_collisions:
                colliding_agent = self.sim.environment.agents[collision.id]
                distance_x = abs(collision.bbox[0] - position.x)
                distance_y = abs(collision.bbox[1] - position.y)
                distance_z = abs(collision.bbox[2] - position.z)
                col_start = max(collision.bbox[3], position.t)
                col_end = min(collision.bbox[7], position.t + real_agent.speed)
                col_time = int(col_end) - int(col_start) + 1

                max_near_distance = real_agent.near_radius

                if isinstance(colliding_agent, PathAgent):
                    max_near_distance += colliding_agent.near_radius

                if distance_x <= max_near_distance and \
                    distance_y <= max_near_distance and \
                    distance_z <= max_near_distance:
                    near_intersections += col_time

        return near_intersections
