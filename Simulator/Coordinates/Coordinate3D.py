import math
from typing import Dict

from .Coordinate2D import Coordinate2D


class Coordinate3D(Coordinate2D):

    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, z)
        self.y: float = y

    def to_dict(self) -> Dict[str, float]:
        return {"x": self.x, "y": self.y, "z": self.z}

    def __repr__(self) -> str:
        return f"({self.x:6.2f}, {self.y:6.2f}, {self.z:6.2f})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and \
               self.y == other.y and \
               self.z == other.z

    def __add__(self, other) -> "Coordinate3D":
        if isinstance(other, Coordinate3D):
            return Coordinate3D(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, Coordinate2D):
            return Coordinate3D(self.x + other.x, self.y, self.z + other.z)
        elif isinstance(other, float) or isinstance(other, int):
            return Coordinate3D(self.x + other, self.y + other, self.z + other)
        else:
            raise Exception(f"Addition is not defined for {other}")

    def __sub__(self, other) -> "Coordinate3D":
        if isinstance(other, Coordinate3D):
            return Coordinate3D(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, Coordinate2D):
            return Coordinate3D(self.x - other.x, self.y, self.z - other.z)
        elif isinstance(other, float) or isinstance(other, int):
            return Coordinate3D(self.x - other, self.y - other, self.z - other)
        else:
            raise Exception(f"Subtraction is not defined for {other}")

    def __mul__(self, other):
        if isinstance(other, Coordinate3D):
            return Coordinate3D(self.x * other.x, self.y * other.y, self.z * other.z)
        if isinstance(other, int) or isinstance(other, float):
            return Coordinate3D(self.x * other, self.y * other, self.z * other)
        else:
            raise Exception(f"Multiplication is not definded for {self.__class__} and {other.__class__}")

    def __truediv__(self, other):
        if isinstance(other, Coordinate3D):
            return Coordinate3D(self.x / other.x, self.y / other.y, self.z / other.z)
        if isinstance(other, int) or isinstance(other, float):
            return Coordinate3D(self.x / other, self.y / other, self.z / other)
        else:
            raise Exception(f"Multiplication is not definded for {self.__class__} and {other.__class__}")

    @property
    def l1(self) -> float:
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def l2(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    @property
    def volume(self) -> float:
        return self.x * self.y * self.z

    def to_2D(self) -> Coordinate2D:
        return Coordinate2D(self.x, self.z)

    def distance(self, other: "Coordinate3D", l2: bool = False) -> float:
        if l2:
            return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5
        else:
            return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def distance_to_space(self, space_min: "Coordinate3D", space_max: "Coordinate3D"):
        # x
        if self.x < space_min.x:
            x = space_min.x
        elif self.x > space_max.x:
            x = space_max.x
        else:
            x = self.x

        # y
        if self.y < space_min.y:
            y = space_min.y
        elif self.y > space_max.y:
            y = space_max.y
        else:
            y = self.y

        # z
        if self.z < space_min.z:
            z = space_min.z
        elif self.z > space_max.z:
            z = space_max.z
        else:
            z = self.z

        return math.sqrt(math.pow(x - self.x, 2) + math.pow(y - self.y, 2) + math.pow(z - self.z, 2))

    def clone(self) -> "Coordinate3D":
        return Coordinate3D(self.x, self.y, self.z)
