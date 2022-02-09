from typing import List, Dict

from simulator.agents.Agent import Agent
from simulator.environments.Environment import Environment
from simulator.fields.EnrichedField import EnrichedField
from simulator.coordinates.TimeCoordinates import TimeCoordinates
from simulator.fields.Field import Field
from simulator.helpers.PathFinding import astar
from simulator.travel_path.TravelPath import TravelPath


class Allocator:
    def __init__(self, env: Environment):
        self.env = env

    def allocate_for_agent(self, agent):
        temporary_allocations: Dict[Agent, TravelPath] = {}
        for _agent in self.env.agents:
            temporary_allocations[_agent] = agent.allocated_path
        resulting_allocations, new_environment = self.allocate_for_agent_rec(agent, self.env, temporary_allocations, [], [])
        self.env.relevant_fields = new_environment.relevant_fields
        for _agent, path in temporary_allocations.items():
            _agent.allocated_path = path

    # It's magic trust me bro
    def allocate_for_agent_rec(self, agent: Agent, local_env: Environment, temporary_allocations: Dict[Agent, TravelPath], assume_coords_blocked: List[TimeCoordinates] = [], assume_coords_free: List[TimeCoordinates] = [] ) -> (Dict[Agent, TravelPath], Environment):
        desired_path = agent.calculate_desired_path()[0] # Todo check for all
        start = desired_path.locations[0]
        for i in range(len(desired_path.locations) - 1):
            end_location = desired_path.locations[i+1]
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
                if field.allocated_to is not None and field.allocated_to != agent:
                    collisions.append(coord)
            if len(collisions) == 0:        # No collision, no cost resolvement
                for coord in optimal_path:
                    field = local_env.get_field_at(coord, True)
                    field.allocated_to = agent
                if agent in temporary_allocations:
                    for coord in temporary_allocations[agent].locations:
                        field = local_env.get_field_at(coord, True)
                        field.allocated_to = None
                temporary_allocations[agent] = TravelPath(optimal_path)
                continue

            collision = collisions[0] # other collisions will be resolved in next recursive call
            field = local_env.get_field_at(collision, False)
            collision_with = field.allocated_to


            # Case if the new agent gets the field
            possible_env_1 = local_env.clone()
            possible_allocations_1, new_agents_winning_env = self.allocate_for_agent_rec(agent, possible_env_1, temporary_allocations, assume_coords_blocked, [collision] + assume_coords_free)
            possible_allocations_1, new_agents_winning_env = self.allocate_for_agent_rec(collision_with, new_agents_winning_env, possible_allocations_1, [collision], [])
            value_for_new_agents_winning_path = agent.value_of_path(possible_allocations_1[agent])
            value_for_current_agent_losing_path = collision_with.value_of_path(possible_allocations_1[collision_with])


            #Value if the new agent doesn't get the field
            possible_env_2 = local_env.clone()
            possible_allocations_2, new_agents_losing_env = self.allocate_for_agent_rec(agent, possible_env_2, temporary_allocations, assume_coords_blocked + [collision], assume_coords_free)
            value_for_new_agents_losing_path = agent.value_of_path(possible_allocations_2[agent])
            value_for_current_agent_winning_path = collision_with.value_of_path(possible_allocations_2[collision_with])


            if value_for_new_agents_winning_path + value_for_current_agent_losing_path > value_for_new_agents_losing_path + value_for_current_agent_winning_path:
                return possible_allocations_1, new_agents_winning_env
            else:
                return possible_allocations_2, new_agents_losing_env

        return temporary_allocations, local_env


    def get_welfare(self, t1: int, t2: int) -> float:
        pass

    def get_field_at(self, coords: TimeCoordinates) -> EnrichedField:
        pass

    def get_cost_of_path(self, path: TravelPath) -> float:
        pass

    def allocate_path_to_agent(self, path: TravelPath, agent: Agent) -> bool:
        pass

    def get_all_active_agents(self) -> List[Agent]:
        pass

    def get_agents_with_collision(self, path: TravelPath) -> List[Agent]:
        pass

    def ask_agents_for_bids(self, agents: List[Agent]):
        pass
