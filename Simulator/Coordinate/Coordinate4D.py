from random import random

from .Coordinate3D import Coordinate3D


class Coordinate4D(Coordinate3D):
    dim = None

    def __init__(self, x: int, y: int, z: int, t: int):
        super().__init__(x, y, z)
        self.t: int = t

    def get_key(self):
        return f"{self.x}_{self.y}_{self.z}_{self.t}"

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z}, {self.t})"

    def __eq__(self, other):
        return self.x == other.x and \
               self.y == other.y and \
               self.z == other.z and \
               self.t == other.t

    def __hash__(self):
        return hash(f"{self.x}:{self.y}:{self.z}:{self.t}")

    def inter_temporal_equal(self, other):
        return super().__eq__(other)

    def tree_query_point_rep(self):
        list_rep = self.list_rep()
        return list_rep + list_rep

    def list_rep(self):
        return [self.x, self.y, self.z, self.t]

    def to_inter_temporal(self):
        return Coordinate3D(self.x, self.y, self.z)

    def __add__(self, other):
        t_other = 0
        if type(other).__name__ == "Coordinate4D":
            t_other = other.t
        return Coordinate4D(self.x + other.x, self.y + other.y, self.z + other.z, self.t + t_other)

    def __sub__(self, other):
        t_other = 0
        if type(other).__name__ == "Coordinate4D":
            t_other = other.t
        return Coordinate4D(self.x - other.x, self.y - other.y, self.z - other.z, self.t - t_other)

    def distance(self, other, l2: bool = False):
        temp = 0
        if isinstance(other, Coordinate4D):
            temp = abs(self.t - other.t)
        return super().distance(other, l2), temp

    def inter_temporal_distance(self, other: Coordinate3D, l2: bool = False) -> float:
        return super().distance(other, l2)

    def clone(self):
        return Coordinate4D(self.x, self.y, self.z, self.t)

    def random_neighbor(self, delta_t=0, chance_x=1 / 3, chance_y=1 / 3, chance_forward=0.5):
        r = random()
        move = 1 if random() > chance_forward else -1
        if r <= chance_x:
            return Coordinate4D(self.x + move, self.y, self.z, self.t + delta_t)
        elif chance_x < r <= chance_y:
            return Coordinate4D(self.x, self.y + move, self.z, self.t + delta_t)
        else:
            return Coordinate4D(self.x, self.y, self.z + move, self.t + delta_t)
