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
        for agent in self.env.agents:
            print(f"{agent}'s non colliding value: {self.non_colliding_value(agent)}, "
                  f"achieved value: {agent.value_for_paths(agent.allocated_paths)}")

    @staticmethod
    def agents_welfare(agent: Agent):
        return agent.value_for_paths(agent.allocated_paths)

    def average_agents_welfare(self):
        summed_welfare = 0
        for agent in self.env.agents:
            summed_welfare += Statistics.agents_welfare(agent)
        print(f"AAW: {summed_welfare/len(self.env.agents)}")
        return summed_welfare / len(self.env.agents)

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
        for agent in self.env.agents:
            for path in agent.allocated_paths:
                length += len(path)
        return length

    def close_passings(self):

        far_field_intersections = [0] * self.env.d
        near_field_intersections = []
        collisions = []
        far_field_crossings = []
        near_field_crossings = []

        for field in self.env.relevant_fields.values():
            if len(field.allocated_to) > 1:
                collisions += 1
            if len(field.far_to) > 1:
                far_field_intersections += len(field.far_to)
            if len(field.near_to) > 1:
                near_field_intersections += len(field.far_to)
            if len(field.allocated_to) >= 1 and len(field.far_to) > 1:
                far_field_crossings += len(field.far_to)
            if len(field.allocated_to) >= 1 and len(field.near_to) > 1:
                near_field_crossings += len(field.near_to)
        print(f"Col: {collisions}, nfc: {near_field_crossings}, nfi: {near_field_intersections}, ffc: {far_field_crossings}, ffi: {far_field_intersections}")
        return collisions, near_field_crossings, near_field_intersections, far_field_crossings, far_field_intersections
