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
        elif isinstance(other, float):
            return Coordinate3D(self.x + other, self.y + other, self.z + other)
        else:
            raise Exception(f"Addition is not defined for {other}")

    def __sub__(self, other) -> "Coordinate3D":
        if isinstance(other, Coordinate3D):
            return Coordinate3D(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, Coordinate2D):
            return Coordinate3D(self.x - other.x, self.y, self.z - other.z)
        elif isinstance(other, float):
            return Coordinate3D(self.x - other, self.y - other, self.z - other)
        else:
            raise Exception(f"Subtraction is not defined for {other}")

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

    def clone(self) -> "Coordinate3D":
        return Coordinate3D(self.x, self.y, self.z)
