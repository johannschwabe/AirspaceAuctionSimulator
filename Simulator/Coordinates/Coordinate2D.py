import math
from typing import Dict


class Coordinate2D:

    def __init__(self, x: int, z: int):
        self.x: int = x
        self.z: int = z

    def to_dict(self) -> Dict[str, int]:
        return {"x": self.x, "z": self.z}

    def __repr__(self) -> str:
        return f"({self.x}, {self.z})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and \
               self.z == other.z

    def __add__(self, other) -> "Coordinate2D":
        if isinstance(other, Coordinate2D):
            return Coordinate2D(self.x + other.x, self.z + other.z)
        elif isinstance(other, int):
            return Coordinate2D(self.x + other, self.z + other)
        else:
            raise Exception(f"Addition is not defined for {other}")

    def __sub__(self, other) -> "Coordinate2D":
        if isinstance(other, Coordinate2D):
            return Coordinate2D(self.x - other.x, self.z - other.z)
        elif isinstance(other, int):
            return Coordinate2D(self.x - other, self.z - other)
        else:
            raise Exception(f"Subtraction is not defined for {other}")

    @property
    def area(self) -> int:
        return self.x * self.z

    @property
    def l1(self) -> int:
        return abs(self.x) + abs(self.z)

    @property
    def l2(self) -> float:
        return math.sqrt(self.x ** 2 + self.z ** 2)

    def distance(self, other: "Coordinate2D", l2: bool = False) -> float:
        if l2:
            return ((self.x - other.x) ** 2 + (self.z - other.z) ** 2) ** 0.5
        else:
            return abs(self.x - other.x) + abs(self.z - other.z)

    def clone(self) -> "Coordinate2D":
        return Coordinate2D(self.x, self.z)

    def __hash__(self):
        return hash((self.x, self.z))
