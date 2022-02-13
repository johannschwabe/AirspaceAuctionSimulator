from typing import List, Dict

from Simulator.Field import Field
from Simulator import Agent, Allocator

cutoff_depth = 6


class FCFSAllocator(Allocator):
    def __init__(self):
        super().__init__()

    def allocate_for_agent(self, agent: Agent):
        costs: Dict[str, float] = {}  # x_y_z_t -> float
        allocated = False
        while not allocated:
            desired_path = agent.calculate_desired_path(costs)
            fields: List[Field] = list(
                map(lambda poi: self.env.get_field_at(poi.to_time_coordinate(), True), desired_path))
            allocated_fields = filter(lambda env_field: not env_field.coordinates.get_key() in costs
                                                        and env_field.is_allocated()
                                                        and not env_field.is_allocated_to == agent,
                                      fields)

            for field in allocated_fields:
                costs[field.coordinates.get_key()] = -1

            else:
                path = list(map(lambda poi: poi.to_time_coordinate, desired_path))
                self.allocate(fields, agent, path)
                allocated = True
