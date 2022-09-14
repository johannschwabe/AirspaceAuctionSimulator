import math
from typing import List, Tuple, Dict

from .Coordinate2D import Coordinate2D
from .Coordinate3D import Coordinate3D


class Coordinate4D(Coordinate3D):
    def __init__(self, x: int | float, y: int | float, z: int | float, t: int):
        super().__init__(x, y, z)
        self.t: int = t

    @staticmethod
    def from_3D(coord_3d: "Coordinate3D", t: int) -> "Coordinate4D":
        return Coordinate4D(coord_3d.x, coord_3d.y, coord_3d.z, t)

    def to_dict(self) -> Dict[str, int | float]:
        return {"x": self.x, "y": self.y, "z": self.z, "t": self.t}

    def __repr__(self) -> str:
        if isinstance(self.x, int):
            str_x = f"{self.x:3d}"
        else:
            str_x = f"{self.x:6.2f}"

        if isinstance(self.y, int):
            str_y = f"{self.y:3d}"
        else:
            str_y = f"{self.y:6.2f}"

        if isinstance(self.z, int):
            str_z = f"{self.z:3d}"
        else:
            str_z = f"{self.x:6.2f}"
        return f"({str_x}, {str_y}, {str_z}, {self.t:3d})"

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

    def __hash__(self) -> int:
        return hash(f"{self.x}:{self.y}:{self.z}:{self.t}")

    def inter_temporal_equal(self, other) -> bool:
        return super().__eq__(other)

    def tree_query_point_rep(self) -> List[int]:
        list_rep = self.list_rep()
        return list_rep + list_rep

    def tree_query_cube_rep(self, radius: int, speed: int) -> List[int]:
        min_corner = [self.x - radius, self.y - radius, self.z - radius, self.t]
        max_corner = [self.x + radius, self.y + radius, self.z + radius, self.t + speed]
        return min_corner + max_corner

    def list_rep(self) -> List[int]:
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
        elif isinstance(other, int):
            return Coordinate4D(self.x + other, self.y + other, self.z + other, self.t + other)
        else:
            raise Exception(f"Addition is not defined for {other}")

    def __sub__(self, other) -> "Coordinate4D":
        if isinstance(other, Coordinate4D):
            return Coordinate4D(self.x - other.x, self.y - other.y, self.z - other.z, self.t - other.t)
        elif isinstance(other, Coordinate3D):
            return Coordinate4D(self.x - other.x, self.y - other.y, self.z - other.z, self.t)
        elif isinstance(other, Coordinate2D):
            return Coordinate4D(self.x - other.x, self.y, self.z - other.z, self.t)
        elif isinstance(other, int):
            return Coordinate4D(self.x - other, self.y - other, self.z - other, self.t - other)
        else:
            raise Exception(f"Subtraction is not defined for {other}")

    def __mul__(self, other):
        if isinstance(other, Coordinate4D):
            return Coordinate4D(self.x * other.x, self.y * other.y, self.z * other.z, self.t * other.t)
        if isinstance(other, int):
            return Coordinate4D(self.x * other, self.y * other, self.z * other, self.t * other)
        else:
            raise Exception(f"Multiplication is not definded for {self.__class__} and {other.__class__}")

    def distance(self, other, l2: bool = False) -> Tuple[float, int]:
        temp = 0
        if isinstance(other, Coordinate4D):
            temp = abs(self.t - other.t)
        return super().distance(other, l2), temp

    @property
    def l1(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z) + abs(self.t)

    @property
    def l2(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2 + self.t ** 2)

    def inter_temporal_distance(self, other: Coordinate3D, l2: bool = False) -> float:
        return super().distance(other, l2)

    def clone(self) -> "Coordinate4D":
        return Coordinate4D(self.x, self.y, self.z, self.t)
