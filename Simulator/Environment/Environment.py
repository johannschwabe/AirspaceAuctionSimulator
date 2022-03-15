from typing import List, Dict

from ..Field import Field
from ..Agent import Agent
from ..Coordinate import TimeCoordinate, Coordinate
from ..IO import Stringify
from ..Time import Tick
from ..Blocker import Blocker


class Environment(Stringify):
    def __init__(self, dimension: Coordinate, blocker: List[Blocker]):
        self._dimension: Coordinate = dimension
        self._agents: List[Agent] = []
        self._relevant_fields: Dict[str, Field] = {}  # x_y_z_t -> Field
        self.blockers: List[Blocker] = blocker

    @staticmethod
    def deallocate_agent(agent: Agent):
        agent._allocated_paths = [[]]
        for field in agent._allocated_fields:
            field._allocated_to.remove(agent)
        for near_field in agent._allocated_near_fields:
            near_field._near_to.remove(agent)
        for far_field in agent._allocated_far_fields:
            far_field._far_to.remove(agent)

    def allocate_paths(self, agent: Agent, paths: List[List[TimeCoordinate]]):
        if agent in self._agents:
            self.deallocate_agent(agent)
        else:
            self._agents.append(agent)

        agent._allocated_paths = paths

        for path in paths:
            for coord in path:
                field: Field = self.get_field_at(coord, True)
                if agent not in field._near_to:
                    field._allocated_to.append(agent)
                if field not in agent._allocated_fields:
                    agent._allocated_fields.append(field)
                # Near border
                for near_coord in agent.get_near_coordinates(coord):
                    near_field: Field = self.get_field_at(near_coord, True)
                    if agent not in near_field._near_to:
                        near_field._near_to.append(agent)
                    if near_field not in agent._allocated_near_fields:
                        agent._allocated_near_fields.append(near_field)
                # Far border
                for far_coord in agent.get_far_coordinates(coord):
                    far_field: Field = self.get_field_at(far_coord, True)
                    if agent not in far_field._far_to:
                        far_field._far_to.append(agent)
                    if far_field not in agent._allocated_far_fields:
                        agent._allocated_far_fields.append(far_field)

    def is_blocked(self, coords: TimeCoordinate) -> bool:
        for blocker in self.blockers:
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
            for near_coord in agent._near_border:
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
        if key in self._relevant_fields:
            return self._relevant_fields[key]
        new_field = Field(coords)
        if creating:
            self._relevant_fields[key] = new_field
        return new_field

    def visualize(self, current_time_step, before=0, nr_steps=1):
        for t in range(current_time_step - before, current_time_step + nr_steps):
            print(f"t = {t}")
            for z in range(self._dimension.z):
                print(f"z={z: >2}", end="")
                for i in range(self._dimension.x):
                    print(f"{i: >4} ", end="")
                print("  -> X")
                for y in range(self._dimension.y):
                    print(f"  {y: >2} ", end="")
                    for x in range(self._dimension.x):
                        coord = TimeCoordinate(x, y, z, Tick(t))
                        field = self.get_field_at(coord, False)
                        if field.is_allocated():
                            if field._allocated_to and t == current_time_step:
                                print(f" {field._allocated_to}".rjust(5, ' '), end="")
                            elif field._allocated_to:
                                print(f"-{field._allocated_to}-".rjust(5, ' '), end="")
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
        new_env = Environment(self._dimension, self.blockers)
        return new_env
