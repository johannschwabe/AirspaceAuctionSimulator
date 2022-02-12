from typing import List, Dict

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

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def is_blocked(self, coords: TimeCoordinate) -> bool:
        for blocker in self.blocker:
            if blocker.is_blocked(coords):
                return True
        return False

    def get_field_at(self, coords: TimeCoordinate, creating: bool) -> Field:
        if coords.get_key() in self.relevant_fields:
            return self.relevant_fields[coords.get_key()]
        new_field = Field(coords)
        if creating:
            self.relevant_fields[coords.get_key()] = new_field
        return new_field

    def visualize(self, current_time_step, before=0, nr_steps=1):
        for t in range(current_time_step - before, current_time_step + nr_steps):
            print(f"t = {t}")
            for z in range(self.dimension.z):
                print(f"z={z: >2}", end="")
                for i in range(self.dimension.x):
                    print(f"{i: >4} ", end="")
                print("  -> X")
                for y in range(self.dimension.y):
                    print(f"  {y: >2} ", end="")
                    for x in range(self.dimension.x):
                        coord = TimeCoordinate(x, y, z, Tick(t))
                        field = self.get_field_at(coord, False)
                        if field.allocated_to is not None and not self.is_blocked(field.coordinates):
                            if field.allocated_to and t == current_time_step:
                                print(f"|{field.allocated_to.uuid}| ".rjust(5, ' '), end="")
                            elif field.allocated_to:
                                print(f"{field.allocated_to.uuid}  ".rjust(5, ' '), end="")
                            elif self.is_blocked(field.coordinates):
                                print("✖  ".rjust(5, ' '), end="")
                        else:
                            print(".  ".rjust(5, ' '), end="")
                    print("")
                print("")
            print(" ↓\n Y")

    def clone(self):
        new_env = Environment(self.dimension, self.blocker)
        new_env.relevant_fields = self.relevant_fields
        return new_env
