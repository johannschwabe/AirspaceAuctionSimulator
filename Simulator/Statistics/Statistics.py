import statistics
from typing import TYPE_CHECKING, List

from ..Agents.PathAgent import PathAgent
from ..Owners.Owner import Owner
from ..Segments.PathSegment import PathSegment

if TYPE_CHECKING:
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Simulator import Simulator
    from ..Agents.Agent import Agent


class Statistics:
    def __init__(self, sim: "Simulator"):
        self.sim: "Simulator" = sim

    def non_colliding_value(self, agent: "Agent"):
        local_agent = agent.initialize_clone()
        local_env = self.sim.environment.new_clear()
        paths = self.sim.mechanism.do([local_agent], local_env, 0)[0]
        return local_agent.value_for_segments(paths.segments)

    def non_colliding_values(self):
        for agent in self.sim.environment.agents.values():
            print(f"{agent}'s non colliding value: {self.non_colliding_value(agent)}, "
                  f"achieved value: {agent.get_allocated_value()}")

    @staticmethod
    def agents_welfare(agent: "Agent"):
        return agent.get_allocated_value()

    def total_agents_welfare(self):
        summed_welfare = 0
        for agent in self.sim.environment.agents.values():
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
        for owner in self.sim.owners:
            summed_welfare += Statistics.owners_welfare(owner)
        print(f"AOW: {summed_welfare / len(self.sim.owners)}")
        return summed_welfare / len(self.sim.owners)

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
