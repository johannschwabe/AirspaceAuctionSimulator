from typing import Dict, List

from simulator.Path import TravelPath
from simulator.agents.Agent import Agent
from simulator.allocators.Allocator import Allocator
from simulator.coordinates import TimeCoordinate
from simulator.environments import Environment
from simulator.helpers.PathFinding import astar


class AllocatorA(Allocator):
    def __init__(self, env: Environment):
        super().__init__(env)

    def allocate_for_agent(self, agent):
        temporary_allocations: Dict[Agent, TravelPath] = {}
        for _agent in self.env.agents:
            temporary_allocations[_agent] = _agent.allocated_path
        resulting_allocations, new_environment = self.allocate_for_agent_rec(agent, self.env, temporary_allocations, [], [])
        self.env.relevant_fields = new_environment.relevant_fields
        self.env.agents.append(agent)
        for _agent, path in resulting_allocations.items():
            _agent.allocated_path = path


    # It's magic trust me bro
    def allocate_for_agent_rec(self, agent: Agent, local_env: Environment, temporary_allocations: Dict[Agent, TravelPath],
                               assume_coords_blocked: List[TimeCoordinate],
                               assume_coords_free: List[TimeCoordinate]) -> (Dict[Agent, TravelPath], Environment):
        if agent in temporary_allocations:
            for coord in temporary_allocations[agent].locations:
                field = local_env.get_field_at(coord, True)
                field.allocated_to = None
            temporary_allocations.pop(agent)
        desired_path = agent.calculate_desired_path()  # Todo check for all
        start = desired_path[0].to_time_coordinate()
        for i in range(len(desired_path) - 1):
            end_location = desired_path[i + 1].to_time_coordinate()
            while start in assume_coords_blocked:  # Illegal start/end positions ugly fix
                start.t += 1
            while end_location in assume_coords_blocked:
                end_location.t += 1
            optimal_path = astar(start,
                                 end_location,
                                 agent,
                                 local_env,
                                 ignore_collisions=True,
                                 assume_coords_free=assume_coords_free,
                                 assume_coords_blocked=assume_coords_blocked)
            collisions = []
            for coord in optimal_path:
                field = local_env.get_field_at(coord, False)
                if field.allocated_to is not None and field.allocated_to != agent and field.coordinates not in assume_coords_free:
                    collisions.append(coord)
            if len(collisions) == 0:  # No collision, no cost resolvement
                for coord in optimal_path:
                    field = local_env.get_field_at(coord, True)
                    field.allocated_to = agent
                if agent in temporary_allocations:
                    temporary_allocations[agent].locations += optimal_path
                else:
                    temporary_allocations[agent] = TravelPath(optimal_path)
                    # for coord in temporary_allocations[agent].locations:
                    # 	field = local_env.get_field_at(coord, True)
                    # 	field.allocated_to = None               # Doesn't work
                # temporary_allocations[agent] = TravelPath(optimal_path)
                if len(optimal_path) == 0:
                    print("no path found")
                start = optimal_path[-1]

                continue
            else:
                collision = collisions[0]  # other collisions will be resolved in next recursive call
                field = local_env.get_field_at(collision, False)
                collision_with = field.allocated_to
                print(f"Collision at {collision} between {collision_with} and {agent}")
                # Case if the new agent gets the field
                possible_env_1 = local_env.clone()
                possible_allocations_1, new_agents_winning_env = self.allocate_for_agent_rec(agent, possible_env_1,
                                                                                             temporary_allocations,
                                                                                             assume_coords_blocked,
                                                                                             [collision.clone()] + assume_coords_free)
                print(f"Allocation for {agent} found")
                possible_allocations_1, new_agents_winning_env = self.allocate_for_agent_rec(collision_with,
                                                                                             new_agents_winning_env,
                                                                                             possible_allocations_1,
                                                                                             [collision.clone()] + assume_coords_free, [])
                value_for_new_agents_winning_path = agent.value_of_path(possible_allocations_1[agent]) # Value of all agent for total welfare
                value_for_current_agent_losing_path = collision_with.value_of_path(possible_allocations_1[collision_with])
                print("Case 2")
                # Case if the new agent doesn't get the field
                possible_env_2 = local_env.clone()
                possible_allocations_2, new_agents_losing_env = self.allocate_for_agent_rec(agent, possible_env_2,
                                                                                            temporary_allocations,
                                                                                            assume_coords_blocked + [collision.clone()],
                                                                                            assume_coords_free)
                value_for_new_agents_losing_path = agent.value_of_path(possible_allocations_2[agent])
                value_for_current_agent_winning_path = collision_with.value_of_path(possible_allocations_2[collision_with])

                if value_for_new_agents_winning_path + value_for_current_agent_losing_path > value_for_new_agents_losing_path + value_for_current_agent_winning_path:
                    return possible_allocations_1, new_agents_winning_env
                else:
                    return possible_allocations_2, new_agents_losing_env

        return temporary_allocations, local_env
