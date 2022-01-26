from typing import List, Dict

from simulator.agents import Agent
from simulator.fields.Field import Field
from simulator.coordinates.Coordinates import Coordinates
from simulator.coordinates.TimeCoordinates import TimeCoordinates


class Environment:
    def __init__(self, dimension: Coordinates):
        self.dimension: Coordinates = dimension
        self.agents: List[Agent] = []
        self.relevant_fields: Dict[str, Field] = {}  # x_y_z_t -> Field

    def is_blocked(self, coords: TimeCoordinates) -> bool:
        pass

    def will_be_blocked(self, coords: TimeCoordinates, t: int) -> float:
        pass

    def get_field_at(self, coords: TimeCoordinates) -> Field:
        pass

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
                        coord = TimeCoordinates(x, y, z, t)
                        field = self.get_field_at(coord)
                        if field:
                            if field.reserved_for and t == current_time_step and coord.inter_temporal_equal(
                                    field.reserved_for.target):
                                print(f"»{field.reserved_for.id}« ".rjust(5, ' '), end="")
                            elif field.reserved_for and t == current_time_step:
                                print(f"|{field.reserved_for.id}| ".rjust(5, ' '), end="")
                            elif field.reserved_for:
                                print(f"{field.reserved_for.id}  ".rjust(5, ' '), end="")
                            elif field.blocked:
                                print("✖  ".rjust(5, ' '), end="")
                        else:
                            print(".  ".rjust(5, ' '), end="")
                    print("")
                print("")
            print(" ↓\n Y")
