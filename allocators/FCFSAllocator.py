from Simulator.helpers.PathFinding import astar
from Simulator import Agent, Environment, Allocator, TravelPath

cutoff_depth = 6


class FCFSAllocator(Allocator):
    def __init__(self):
        super().__init__()

    def allocate_for_agent(self, agent: Agent, env: Environment):
        desired_path = agent.calculate_desired_path()
        start = desired_path[0].to_time_coordinate()
        target = desired_path[-1].to_time_coordinate()
        optimal_path = astar(start,
                             target,
                             agent,
                             env,
                             assume_coords_free=[],
                             assume_coords_blocked=[])

        for coord in optimal_path:
            field = env.get_field_at(coord, True)
            field.allocated_to = agent

        env.add_agent(agent)
        agent.allocated_path = TravelPath(optimal_path)

