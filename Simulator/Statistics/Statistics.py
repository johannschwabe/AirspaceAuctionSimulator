from ..Simulator import Owner
from ..Simulator import Simulator
from ..Agent import Agent


class Statistics:
    def __init__(self, sim: Simulator):
        self.env = sim.environment
        self.allocator = sim.allocator
        self.history = sim.history
        self.owners = sim.owners
        self.time_elapsed = sim.time_step

    def non_colliding_value(self, agent: Agent):
        local_agent = agent.clone()
        local_env = self.env.clear()
        paths = self.allocator.allocate_for_agents([local_agent], local_env)[local_agent]
        return local_agent.value_for_paths(paths)

    def non_colliding_values(self):
        for agent in self.env.get_agents():
            print(f"{agent}'s non colliding value: {self.non_colliding_value(agent)}, "
                  f"achieved value: {agent.get_allocated_value()}")

    @staticmethod
    def agents_welfare(agent: Agent):
        return agent.get_allocated_value()

    def average_agents_welfare(self):
        summed_welfare = 0
        for agent in self.env.get_agents():
            summed_welfare += Statistics.agents_welfare(agent)
        print(f"AAW: {summed_welfare/len(self.env.get_agents())}")
        return summed_welfare / len(self.env.get_agents())

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
        for agent in self.env.get_agents():
            for path in agent.allocated_paths:
                length += len(path)
        return length

    def close_passings(self):
        far_field_intersections = [0] * self.env._dimension.t
        near_field_intersections = [0] * self.env._dimension.t
        collisions = [0] * self.env._dimension.t
        far_field_crossings = [0] * self.env._dimension.t
        near_field_crossings = [0] * self.env._dimension.t

        for field in self.env._relevant_fields.values():
            if len(field.get_allocated()) > 1:
                collisions[field.coordinates.t] += 1
            if len(field.get_far()) > 1:
                far_field_intersections[field.coordinates.t] += len(field.get_far())
            if len(field.get_near()) > 1:
                near_field_intersections[field.coordinates.t] += len(field.get_near())
            if len(field.get_allocated()) >= 1 and len(field.get_far()) > 1:
                far_field_crossings[field.coordinates.t] += len(field.get_far())
            if len(field.get_allocated()) >= 1 and len(field.get_near()) > 1:
                near_field_crossings[field.coordinates.t] += len(field.get_near())
        print(f"Col: {sum(collisions)}, nfc: {sum(near_field_crossings)}, nfi: {sum(near_field_intersections)}, ffc: {sum(far_field_crossings)}, ffi: {sum(far_field_intersections)}")
        return collisions, near_field_crossings, near_field_intersections, far_field_crossings, far_field_intersections
