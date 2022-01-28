
from abc import ABC, abstractmethod
from Agent import Agent
from Field import Field
from coords import Coords



class Environment(ABC):
    def __init__(self):
        self.agents = []
        self.fields = {}         # x_y_z_t -> Field

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def add_agent(self, agent: Agent, time_step):
        pass

    def is_blocked(self, coords):
        intertemporal_block_key = f"{coords.x}_{coords.y}_{coords.z}_-1"
        if intertemporal_block_key in self.fields and self.fields[intertemporal_block_key].blocked:
            return self.fields[intertemporal_block_key]
        return None

    def block(self, coords):
        intertemporal_block_key = f"{coords.x}_{coords.y}_{coords.z}_-1"
        new_field = Field()
        new_field.blocked = True
        self.fields[intertemporal_block_key] = new_field

    def get_field(self, coords, creating):
        blocked = self.is_blocked(coords)
        if blocked:
            return blocked
        key = coords.get_key()
        if key not in self.fields:
            if creating:
                new_field = Field()
                self.fields[key] = new_field
            else:
                return None
        return self.fields[key]
    @abstractmethod
    def move(self):
        pass

    def visualize(self, current_time_step, before = 0, nr_steps=1):
        for t in range(current_time_step - before, current_time_step+nr_steps):
            print(f"t = {t}")
            for z in range(Coords.dim_z):
                print(f"z={z: >2}", end="")
                for i in range(Coords.dim_x):
                    print(f"{i: >4} ", end="")
                print("  -> X")
                for y in range(Coords.dim_y):
                    print(f"  {y: >2} ", end="")
                    for x in range(Coords.dim_x):
                        coord = Coords(x,y,z,t)
                        field = self.get_field(coord, False)
                        if field:
                            if field.reserved_for and t == current_time_step and coord.intertemporal_equal(field.reserved_for.target):
                                print(f"»{field.reserved_for.id}« ".rjust(5,' '), end="")
                            elif field.reserved_for and t == current_time_step:
                                print(f"|{field.reserved_for.id}| ".rjust(5,' '), end="")
                            elif field.reserved_for:
                                print(f"{field.reserved_for.id}  ".rjust(5,' '), end="")
                            elif field.blocked:
                                print("✖  ".rjust(5,' '), end="")
                        else:
                            print(".  ".rjust(5,' '), end="")
                    print("")
                print("")
            print(" ↓\n Y")




