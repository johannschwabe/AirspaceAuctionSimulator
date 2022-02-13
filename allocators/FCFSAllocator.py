from typing import List

from Simulator.Coordinate import TimeCoordinate
from Simulator.Field import EnrichedField
from Simulator.helpers.PathFinding import astar
from Simulator import Agent, Environment, Allocator, TravelPath

cutoff_depth = 6


class FCFSAllocator(Allocator):
    def __init__(self, env):
        super().__init__(env)

    def allocate_for_agent(self, agent: Agent):
        desired_path = agent.calculate_desired_path(self)
        fields = list(map(lambda poi: self.env.get_field_at(poi.to_time_coordinate(), True), desired_path))
        occupied_fields = list(map(lambda env_field: env_field.is_allocated(), fields))

        if len(occupied_fields) > 0:
            occupied_coords = list(map(lambda field: EnrichedField(field.coordinates, -1), occupied_fields))
            return False, occupied_coords
        else:
            desired_coords = list(map(lambda poi: poi.to_time_coordinate, desired_path))
            self.allocate(fields, agent, desired_coords)
            return True, desired_coords
