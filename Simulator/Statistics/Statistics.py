from ..Environment import Environment
from ..History2 import HistoryAgent
from ..Simulator import Owner
from ..Simulator import Simulator
from ..Agent import Agent
from ..Coordinate import TimeCoordinate

class Statistics:
    def __init__(self, sim: Simulator):
        self.history = sim.history

    def non_colliding_value(self, agent: Agent):
        local_agent = agent.clone()
        local_env = self.history.env.new_clear()
        paths = self.history.allocator.allocate_for_agents([local_agent], local_env)[local_agent]
        return local_agent.value_for_paths(paths)

    def non_colliding_values(self):
        for agent in self.history.env.get_agents().values():
            print(f"{agent}'s non colliding value: {self.non_colliding_value(agent)}, "
                  f"achieved value: {agent.get_allocated_value()}")

    @staticmethod
    def agents_welfare(agent: Agent):
        return agent.get_allocated_value()

    def average_agents_welfare(self):
        summed_welfare = 0
        for agent in self.history.env.get_agents().values():
            summed_welfare += Statistics.agents_welfare(agent)
        print(f"AAW: {summed_welfare/len(self.history.env.get_agents())}")
        return summed_welfare / len(self.history.env.get_agents())

    @staticmethod
    def owners_welfare(owner: Owner):
        summed_welfare = 0
        for agent in owner.agents:
            summed_welfare += Statistics.agents_welfare(agent)
        return summed_welfare

    def average_owners_welfare(self):
        summed_welfare = 0
        for owner in self.history.owners:
            summed_welfare += Statistics.owners_welfare(owner)
        print(f"AOW: {summed_welfare/len(self.history.owners)}")
        return summed_welfare/len(self.history.owners)

    def allocated_distance(self):
        length = 0
        for agent in self.history.env.get_agents():
            for path in agent.allocated_paths:
                length += len(path)
        return length

    def close_passings(self):
        res = {}
        for agent in self.history.env.get_agents().values():
            res[agent.id] = {
                "near_field_violations": {},
                "near_field_intersection": {},
                "far_field_violations": {},
                "far_field_intersection": {},
            }
            for path in agent.get_allocated_paths():
                for step in path[::agent.speed]:
                    res[agent.id]["near_field_violations"][step.t] = self.violations(step, agent, agent.near_radius)
                    res[agent.id]["far_field_violations"][step.t] = self.violations(step, agent, agent.far_radius)
                    near_intersections, far_intersections = self.intersections(step, agent)
                    res[agent.id]["near_field_intersection"][step.t] = near_intersections
                    res[agent.id]["far_field_intersection"][step.t] = far_intersections
        return res

    def violations(self, position: TimeCoordinate, agent: HistoryAgent, radi: int):
        box = [  position.x - radi,
                 position.y - radi,
                 position.z - radi,
                 position.t,
                 position.x + radi,
                 position.y + radi,
                 position.z + radi,
                 position.t + agent.speed -1]
        collisions = self.history.env.tree.intersection(box, objects=True)
        real_collisions = filter(lambda col: col.id != agent.id, collisions)
        count = 0
        for real_collision in real_collisions:
            start = max(real_collision.bbox[3], position.t)
            end = min(real_collision.bbox[7], position.t + agent.speed - 1)
            count += int(end) - int(start) + 1
        return count

    def intersections(self, position: TimeCoordinate, agent: HistoryAgent):
        max_radi = self.history.env.get_agents()[agent.id].max_far_field_radius
        near_radi = self.history.env.get_agents()[agent.id].near_radius
        fahrrad = self.history.env.get_agents()[agent.id].far_radius
        box = [  position.x - max_radi * 2,
                 position.y - max_radi * 2,
                 position.z - max_radi * 2,
                 position.t,
                 position.x + max_radi * 2,
                 position.y + max_radi * 2,
                 position.z + max_radi * 2,
                 position.t + agent.speed - 1]
        collisions = self.history.env.tree.intersection(box, objects=True)
        real_collisions = filter(lambda col: col.id != agent.id, collisions)
        near_intersections = 0
        far_intersections = 0
        for collision in real_collisions:
            distance_x = abs(collision.bbox[0] - position.x)
            distance_y = abs(collision.bbox[1] - position.y)
            distance_z = abs(collision.bbox[2] - position.z)
            col_start = max(collision.bbox[3], position.t)
            col_end = min(collision.bbox[7], position.t + agent.speed - 1)
            col_time = int(col_end) - int(col_start) + 1
            max_near_distance = near_radi + self.history.env.get_agents()[collision.id].near_radius
            max_far_distance = fahrrad + self.history.env.get_agents()[collision.id].far_radius
            if distance_x <= max_near_distance and distance_y <= max_near_distance and distance_z <= max_near_distance:
                near_intersections +=  col_time
            if distance_x <= max_far_distance and distance_y <= max_far_distance and distance_z <= max_far_distance:
                far_intersections += col_time

        return near_intersections, far_intersections


    # def close_passings(self):
    #     max_t = int(float(self.env._dimension.t) * 1.5)
    #     far_field_intersections = [0] * max_t
    #     near_field_intersections = [0] * max_t
    #     collisions = [0] * max_t
    #     far_field_crossings = [0] * max_t
    #     near_field_crossings = [0] * max_t
    #
    #     for field in self.env._relevant_fields.values():
    #         if len(field.get_allocated()) > 1:
    #             collisions[field.coordinates.t] += 1
    #         if len(field.get_far()) > 1:
    #             far_field_intersections[field.coordinates.t] += len(field.get_far())
    #         if len(field.get_near()) > 1:
    #             near_field_intersections[field.coordinates.t] += len(field.get_near())
    #         if len(field.get_allocated()) >= 1 and len(field.get_far()) > 1:
    #             far_field_crossings[field.coordinates.t] += len(field.get_far())
    #         if len(field.get_allocated()) >= 1 and len(field.get_near()) > 1:
    #             near_field_crossings[field.coordinates.t] += len(field.get_near())
    #     print(f"Col: {sum(collisions)}, nfc: {sum(near_field_crossings)}, nfi: {sum(near_field_intersections)}, ffc: {sum(far_field_crossings)}, ffi: {sum(far_field_intersections)}")
    #     return collisions, near_field_crossings, near_field_intersections, far_field_crossings, far_field_intersections
