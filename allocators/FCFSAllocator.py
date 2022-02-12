from typing import List

from Simulator.Coordinate import TimeCoordinate
from Simulator.helpers.PathFinding import astar
from Simulator import Agent, Environment, Allocator, TravelPath

cutoff_depth = 6


class FCFSAllocator(Allocator):
    def __init__(self):
        super().__init__()

    def allocate_for_agent(self, agent: Agent, env: Environment):
        optimal_path: List[TimeCoordinate] = []
        desired_path = agent.calculate_desired_path()
        start = desired_path[0].to_time_coordinate()
        for poi in desired_path[1:]:
            target = poi.to_time_coordinate()
            optimal_path.extend(astar(start,
                                      target,
                                      agent,
                                      env,
                                      assume_coords_free=[],
                                      assume_coords_blocked=[]))
            start = poi.to_time_coordinate()

        for coord in optimal_path:
            field = env.get_field_at(coord, True)
            field.allocated_to = agent

        env.add_agent(agent)
        agent.allocated_path = TravelPath(optimal_path)
