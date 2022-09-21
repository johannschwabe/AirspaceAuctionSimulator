import math
from typing import List, Dict

from .Coordinate2D import Coordinate2D
from .Coordinate3D import Coordinate3D


class Coordinate4D(Coordinate3D):
    def __init__(self, x: float, y: float, z: float, t: int):
        super().__init__(x, y, z)
        self.t: int = t

    @staticmethod
    def from_3D(coord_3d: "Coordinate3D", t: int) -> "Coordinate4D":
        return Coordinate4D(coord_3d.x, coord_3d.y, coord_3d.z, t)

    def to_dict(self) -> Dict[str, float]:
        return {"x": self.x, "y": self.y, "z": self.z, "t": self.t}

    def __repr__(self) -> str:
        return f"({self.x:6.2f}, {self.y:6.2f}, {self.z:6.2f}, {self.t:3d})"

    def __str__(self):
        return f"({self.x:3d}, {self.y:3d}, {self.z:3d}, {self.t:3d})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and \
               self.y == other.y and \
               self.z == other.z and \
               self.t == other.t

    def __lt__(self, other) -> bool:
        return self.x < other.x and \
               self.y < other.y and \
               self.z < other.z and \
               self.t < other.t

    def __gt__(self, other) -> bool:
        return self.x > other.x and \
               self.y > other.y and \
               self.z > other.z and \
               self.t > other.t

    def __ge__(self, other) -> bool:
        return self.x >= other.x and \
               self.y >= other.y and \
               self.z >= other.z and \
               self.t >= other.t

    def __le__(self, other) -> bool:
        return self.x <= other.x and \
               self.y <= other.y and \
               self.z <= other.z and \
               self.t <= other.t

    def __hash__(self) -> float:
        return hash(f"{self.x}:{self.y}:{self.z}:{self.t}")

    def inter_temporal_equal(self, other) -> bool:
        return super().__eq__(other)

    def tree_query_point_rep(self) -> List[float]:
        list_rep = self.list_rep()
        return list_rep + list_rep

    def tree_query_cube_rep(self, radius: float, speed: float) -> List[float]:
        min_corner = [self.x - radius, self.y - radius, self.z - radius, self.t]
        max_corner = [self.x + radius, self.y + radius, self.z + radius, self.t + speed]
        return min_corner + max_corner

    def list_rep(self) -> List[float]:
        return [self.x, self.y, self.z, self.t]

    def to_3D(self) -> "Coordinate3D":
        return Coordinate3D(self.x, self.y, self.z)

    def __add__(self, other) -> "Coordinate4D":
        if isinstance(other, Coordinate4D):
            return Coordinate4D(self.x + other.x, self.y + other.y, self.z + other.z, self.t + other.t)
        elif isinstance(other, Coordinate3D):
            return Coordinate4D(self.x + other.x, self.y + other.y, self.z + other.z, self.t)
        elif isinstance(other, Coordinate2D):
            return Coordinate4D(self.x + other.x, self.y, self.z + other.z, self.t)
        elif isinstance(other, float) or isinstance(other, int):
            return Coordinate4D(self.x + other, self.y + other, self.z + other, self.t)
        else:
            raise Exception(f"Addition is not defined for {other}")

    def __sub__(self, other) -> "Coordinate4D":
        if isinstance(other, Coordinate4D):
            return Coordinate4D(self.x - other.x, self.y - other.y, self.z - other.z, self.t - other.t)
        elif isinstance(other, Coordinate3D):
            return Coordinate4D(self.x - other.x, self.y - other.y, self.z - other.z, self.t)
        elif isinstance(other, Coordinate2D):
            return Coordinate4D(self.x - other.x, self.y, self.z - other.z, self.t)
        elif isinstance(other, float) or isinstance(other, int):
            return Coordinate4D(self.x - other, self.y - other, self.z - other, self.t)
        else:
            raise Exception(f"Subtraction is not defined for {other}")

    @property
    def l1(self) -> float:
        return abs(self.x) + abs(self.y) + abs(self.z) + abs(self.t)

    @property
    def l2(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2 + self.t ** 2)

    def clone(self) -> "Coordinate4D":
        return Coordinate4D(self.x, self.y, self.z, self.t)
