import statistics

from ..Path import PathSegment
from typing import TYPE_CHECKING, List
from ..Agent import PathAgent

if TYPE_CHECKING:
    from ..Coordinate import Coordinate4D
    from .. import Simulator, Owner
    from ..Agent import Agent
    from ..History import HistoryAgent, History


class Statistics:
    def __init__(self, sim: "Simulator"):
        self.history: "History" = sim.history

    def non_colliding_value(self, agent: "Agent"):
        local_agent = agent.clone()
        local_env = self.history.env.new_clear()
        paths = self.history.allocator.allocate_for_agents([local_agent], local_env, 0)[0]
        return local_agent.value_for_segments(paths.segments)

    def non_colliding_values(self):
        for agent in self.history.env.get_agents().values():
            print(f"{agent}'s non colliding value: {self.non_colliding_value(agent)}, "
                  f"achieved value: {agent.get_allocated_value()}")

    @staticmethod
    def agents_welfare(agent: "Agent"):
        return agent.get_allocated_value()

    def total_agents_welfare(self):
        summed_welfare = 0
        for agent in self.history.env.get_agents().values():
            summed_welfare += Statistics.agents_welfare(agent)
        return summed_welfare

    @staticmethod
    def owners_welfare(owner: "Owner"):
        summed_welfare = 0
        for agent in owner.agents:
            summed_welfare += Statistics.agents_welfare(agent)
        return summed_welfare

    def average_owners_welfare(self):
        summed_welfare = 0
        for owner in self.history.owners:
            summed_welfare += Statistics.owners_welfare(owner)
        print(f"AOW: {summed_welfare / len(self.history.owners)}")
        return summed_welfare / len(self.history.owners)

    def allocated_distance(self):
        length = 0
        for agent in self.history.env.get_agents():
            for path in agent.allocated_paths:
                length += len(path)
        return length

    @staticmethod
    def path_statistics(path: List["Coordinate4D"]):
        ascended = 0
        descended = 0
        distance = 0
        heights = []
        median_height = -1
        average_height = -1
        if len(path) > 0:
            last = path[0]
            for coord in path:
                if not coord.inter_temporal_equal(last):
                    distance += abs(coord.x - last.x) + abs(coord.z - last.z)
                    delta = coord.y - last.y
                    if delta > 0:
                        ascended += delta
                    else:
                        descended += delta
                heights.append(coord.y)
                last = coord

            median_height = statistics.median(heights)
            average_height = statistics.mean(heights)
        return {
            "asc": ascended,
            "desc": descended,
            "dist": distance,
            "med_height": median_height,
            "avg_height": average_height
        }

    def close_encounters(self):
        res = {}
        far_radi = [_agent.far_radius for _agent in self.history.env.get_agents().values() if
                    isinstance(_agent, PathAgent)]
        far_radi.append(0)
        max_far_radi = max(far_radi)

        near_radi = [_agent.near_radius for _agent in self.history.env.get_agents().values() if
                     isinstance(_agent, PathAgent)]
        near_radi.append(0)
        max_near_radi = max(near_radi)

        for agent in self.history.env.get_agents().values():
            res[agent.id] = {
                "near_field_violations": {},
                "near_field_intersection": {},
                "far_field_violations": {},
                "far_field_intersection": {},
                "total_near_field_violations": 0,
                "total_near_field_intersection": 0,
                "total_far_field_violations": 0,
                "total_far_field_intersection": 0,
            }
            for segment in agent.get_allocated_segments():
                if isinstance(segment, PathSegment):
                    for step in segment[::agent.speed]:
                        res[agent.id]["near_field_violations"][step.t] = self.violations(step, agent, agent.near_radius)
                        res[agent.id]["far_field_violations"][step.t] = self.violations(step, agent, agent.far_radius)
                        near_intersections, far_intersections = \
                            self.intersections(step, agent, max_far_radi, max_near_radi)
                        res[agent.id]["near_field_intersection"][step.t] = near_intersections
                        res[agent.id]["far_field_intersection"][step.t] = far_intersections
                        res[agent.id]["total_near_field_violations"] += res[agent.id]["near_field_violations"][step.t]
                        res[agent.id]["total_far_field_violations"] += res[agent.id]["far_field_violations"][step.t]
                        res[agent.id]["total_near_field_intersection"] += res[agent.id]["near_field_intersection"][
                            step.t]
                        res[agent.id]["total_far_field_intersection"] += res[agent.id]["far_field_intersection"][step.t]
        return res

    def violations(self, position: "Coordinate4D", agent: "HistoryAgent", radi: int):
        box = [position.x - radi,
               position.y - radi,
               position.z - radi,
               position.t,
               position.x + radi,
               position.y + radi,
               position.z + radi,
               position.t + agent.speed - 1]
        collisions = self.history.env.tree.intersection(box, objects=True)
        real_collisions = filter(lambda col: col.id != agent.id, collisions)
        count = 0
        for real_collision in real_collisions:
            start = max(real_collision.bbox[3], position.t)
            end = min(real_collision.bbox[7], position.t + agent.speed - 1)
            count += int(end) - int(start) + 1
        return count

    def intersections(self, position: "Coordinate4D", agent: "Agent", max_far_radi, max_near_radi):
        near_intersections = 0
        far_intersections = 0
        real_agent: "Agent" = self.history.env.get_agents()[agent.id]
        if isinstance(real_agent, PathAgent):
            box = [position.x - max_far_radi,
                   position.y - max_far_radi,
                   position.z - max_far_radi,
                   position.t,
                   position.x + max_far_radi,
                   position.y + max_far_radi,
                   position.z + max_far_radi,
                   position.t + real_agent.speed]
            collisions = self.history.env.tree.intersection(box, objects=True)
            real_collisions = filter(lambda col: col.id != agent.id, collisions)

            for collision in real_collisions:
                colliding_agent = self.history.env.get_agents()[collision.id]
                distance_x = abs(collision.bbox[0] - position.x)
                distance_y = abs(collision.bbox[1] - position.y)
                distance_z = abs(collision.bbox[2] - position.z)
                col_start = max(collision.bbox[3], position.t)
                col_end = min(collision.bbox[7], position.t + real_agent.speed)
                col_time = int(col_end) - int(col_start) + 1

                max_near_distance = real_agent.near_radius
                max_far_distance = real_agent.far_radius

                if isinstance(colliding_agent, PathAgent):
                    max_near_distance += colliding_agent.near_radius
                    max_far_distance += colliding_agent.far_radius

                if distance_x <= max_near_distance and \
                    distance_y <= max_near_distance and \
                    distance_z <= max_near_distance:
                    near_intersections += col_time

                if distance_x <= max_far_distance and \
                    distance_y <= max_far_distance and \
                    distance_z <= max_far_distance:
                    far_intersections += col_time

        return near_intersections, far_intersections
