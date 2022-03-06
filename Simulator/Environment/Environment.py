from typing import List, Dict

from ..Environment import TempEnvironment
from ..Field import Field
from ..Agent import Agent
from ..Coordinate import TimeCoordinate, Coordinate
from ..Time import Tick
from ..Blocker import Blocker


class Environment:
    def __init__(self, dimension: Coordinate, blocker: List[Blocker]):
        self.dimension: Coordinate = dimension
        self.agents: List[Agent] = []
        self.relevant_fields: Dict[str, Field] = {}  # x_y_z_t -> Field
        self.blocker: List[Blocker] = blocker

    @staticmethod
    def deallocate_agent(agent: Agent, time_step: Tick):
        agent.allocated_paths = [[]]
        for field in agent.allocated_fields:
            if field.coordinates.t > time_step:
                field.allocated_to.remove(agent)
        for near_field in agent.allocated_near_fields:
            if near_field.coordinates.t > time_step:
                near_field.near_to.remove(agent)
        for far_field in agent.allocated_far_fields:
            if far_field.coordinates.t > time_step:
                far_field.far_to.remove(agent)

    def allocate_path(self, agent:Agent, path: List[List[TimeCoordinate]]):
        agent.allocated_paths = path

        for path in path:
            for coord in path:
                field: Field = self.get_field_at(coord, True)
                if agent not in field.near_to:
                    field.allocated_to.append(agent)
                if field not in agent.allocated_fields:
                    agent.allocated_fields.append(field)
                # Near border
                for near_coord in agent.get_near_coordinates(coord):
                    near_field: Field = self.get_field_at(near_coord, True)
                    if agent not in near_field.near_to:
                        near_field.near_to.append(agent)
                    if near_field not in agent.allocated_near_fields:
                        agent.allocated_near_fields.append(near_field)
                # Far border
                for far_coord in agent.get_far_coordinates(coord):
                    far_field: Field = self.get_field_at(far_coord, True)
                    if agent not in far_field.far_to:
                        far_field.far_to.append(agent)
                    if far_field not in agent.allocated_far_fields:
                        agent.allocated_far_fields.append(far_field)

    def allocate_paths(self, agents_paths: Dict[Agent, List[List[TimeCoordinate]]], time_step: Tick):
        for agent, paths in agents_paths.items():
            if agent in self.agents:
                self.deallocate_agent(agent, time_step)
            else:
                self.agents.append(agent)
            self.allocate_path(agent, paths)

    def is_blocked(self, coords: TimeCoordinate) -> bool:
        for blocker in self.blocker:
            if blocker.is_blocked(coords):
                return True
        return False

    def is_valid_for_allocation(self, coords: TimeCoordinate, agent: Agent) -> bool:
        is_free = True
        for t in range(agent.speed):
            waiting_coord = TimeCoordinate(coords.x, coords.y, coords.z, coords.t + Tick(t))
            # Blocker
            if self.is_blocked(waiting_coord):
                is_free = False
                break
            # Allocated to or in near boarder of other agents
            field = self.get_field_at(waiting_coord, False)
            if field.is_allocated() or field.is_near():
                is_free = False
                break
            # Other agent in near border
            for near_coord in agent.near_border:
                near_neighbor = TimeCoordinate(near_coord.x, near_coord.y, near_coord.z, waiting_coord.t)
                near_field = self.get_field_at(near_neighbor, False)
                if near_field.is_allocated():
                    is_free = False
                    break

            if not is_free:
                break

        return is_free


    def get_field_at(self, coords: TimeCoordinate, creating: bool) -> Field:
        key = coords.get_key()
        if key in self.relevant_fields:
            return self.relevant_fields[key]
        new_field = Field(coords)
        if creating:
            self.relevant_fields[key] = new_field
        return new_field

    def visualize(self, current_time_step, before=0, nr_steps=1):
        for t in range(current_time_step - before, current_time_step + nr_steps):
            print(f"t = {t}")
            for z in range(self.dimension.z):
                print(f"z={z: >2}", end="")
                for i in range(self.dimension.x):
                    print(f" {i: >4}", end="")
                print("  -> X")
                for y in range(self.dimension.y):
                    print(f"  {y: >2} ", end="")
                    for x in range(self.dimension.x):
                        coord = TimeCoordinate(x, y, z, Tick(t))
                        field = self.get_field_at(coord, False)
                        if field.is_allocated():
                            if field.allocated_to and t == current_time_step:
                                print(f" {field.allocated_to}".rjust(5, ' '), end="")
                            elif field.allocated_to:
                                print(f"-{field.allocated_to}-".rjust(5, ' '), end="")
                        elif self.is_blocked(field.coordinates):
                            print("✖".rjust(5, ' '), end="")
                        elif field.is_near():
                            print("*".rjust(5, ' '), end="")
                        elif field.is_far():
                            print("-".rjust(5, ' '), end="")
                        else:
                            print(".".rjust(5, ' '), end="")
                    print("")
                print("")
            print(" ↓\n Y")

    def clear(self):
        new_env = Environment(self.dimension, self.blocker)
        return new_env

    def generate_temporary_env(self):
        return TempEnvironment.TempEnvironment(self)

