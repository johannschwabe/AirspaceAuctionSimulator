import math
from random import randint


class Coordinate2D:

    def __init__(self, x: int, z: int):
        self.x: int = x
        self.z: int = z

    def get_key(self):
        return f"{self.x}_{self.z}"

    def __repr__(self):
        return f"({self.x}, {self.z})"

    def __eq__(self, other):
        return self.x == other.x and \
               self.z == other.z

    def __add__(self, other):
        return Coordinate2D(self.x + other.x, self.z + other.z)

    def __sub__(self, other):
        return Coordinate2D(self.x - other.x, self.z - other.z)

    @property
    def l1(self):
        return abs(self.x) + abs(self.z)

    @property
    def l2(self):
        return math.sqrt(self.x ** 2 + self.z ** 2)

    def distance(self, other, l2: bool = False):
        if l2:
            return ((self.x - other.x) ** 2 + (self.z - other.xz) ** 2) ** 0.5
        else:
            return abs(self.x - other.x) + abs(self.z - other.z)

    def clone(self):
        return Coordinate2D(self.x, self.z)
