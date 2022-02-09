from typing import List

from simulator.agents.Agent import Agent
from simulator.environments.Environment import Environment
from simulator.fields.EnrichedField import EnrichedField
from simulator.coordinates.TimeCoordinates import TimeCoordinates
from simulator.helpers.PathFinding import astar
from simulator.travel_path.TravelPath import TravelPath


class Allocator:
    def __init__(self, env: Environment):
        self.env = env

    # It's magic trust me bro
    def allocate_for_agent(self, agent: Agent, assume_coords_blocked: List[TimeCoordinates] = [], assume_coords_free: List[TimeCoordinates] = []) -> TravelPath:
        desired_path = agent.calculate_desired_path()[0] # Todo check for all
        start = desired_path.locations[0]
        allocated_path = []
        for i in range(len(desired_path.locations) - 1):
            end_location = desired_path.locations[i+1]
            optimal_path = astar(start,
                                 end_location,
                                 agent,
                                 self.env,
                                 ignore_collisions=True,
                                 assume_coords_free=assume_coords_free,
                                 assume_coords_blocked=assume_coords_blocked)
            collisions = []
            for coord in optimal_path:
                field = self.env.get_field_at(coord, False)
                if field.allocated_to is not None:
                    collisions.append(coord)
            if len(collisions) == 0:        # No collision, no cost resolvement
                for coord in optimal_path:
                    field = self.env.get_field_at(coord, True)
                    field.allocated_to = agent
                return TravelPath(optimal_path)

            collision = collisions[0] # other collisions will be resolved in next recursive call
            field = self.env.get_field_at(collision, False)
            collision_with = field.allocated_to

            # Value if the currently allocated to agent keeps the field
            current_value_for_path = collision_with.value_of_path(collision_with.allocated_path)

            # Value if the currently allocated to agent gives up the field
            alternative_path = self.allocate_for_agent(collision_with, [collision])
            value_for_alternative_path = collision_with.value_of_path(alternative_path)

            current_agents_cost_of_losing = current_value_for_path - value_for_alternative_path

            # Value if the new agent gets the field
            new_agents_winning_path = self.allocate_for_agent(agent, assume_coords_blocked, assume_coords_free + [collision])
            value_for_new_agents_winning_path = agent.value_of_path(new_agents_winning_path)

            #Value if the new agent doesn't get the field
            new_agents_losing_path = self.allocate_for_agent(agent, assume_coords_blocked + [collision], assume_coords_free)
            value_for_new_agents_losing_path = agent.value_of_path(new_agents_losing_path)

            new_agents_cost_of_losing = value_for_new_agents_winning_path - value_for_new_agents_losing_path

            if current_agents_cost_of_losing > new_agents_cost_of_losing:
                allocated_path += new_agents_losing_path
            allocated_path += new_agents_winning_path
            for coords in collision_with.allocated_path.locations:


            start = allocated_path[-1]

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
