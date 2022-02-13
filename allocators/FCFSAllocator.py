from typing import List

from Simulator.Coordinate import TimeCoordinate
from Simulator.helpers.PathFinding import astar
from Simulator import Agent, Environment, Allocator, TravelPath

cutoff_depth = 6


class FCFSAllocator(Allocator):
    def __init__(self, env):
        super().__init__(env)

    def get_shortest_path(self, start: TimeCoordinate, target: TimeCoordinate):
        return astar(start,
                     target,
                     self.env)

    def allocate_for_agent(self, agent: Agent, env: Environment):
        optimal_path: List[TimeCoordinate] = []
        desired_path = agent.calculate_desired_path(self)
        for poi in desired_path:
            coord = TimeCoordinate(poi.location.x, poi.location.y, poi.location.z, poi.tick)
            field = env.get_field_at(coord, True)
            field.allocated_to = agent

        env.add_agent(agent)
        agent.allocated_path = TravelPath(optimal_path)
