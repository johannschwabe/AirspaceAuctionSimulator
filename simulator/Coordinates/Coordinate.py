import math


class Coordinate:

    def __init__(self, x: int, y: int, z: int):
        self.x: int = x
        self.y: int = y
        self.z: int = z

    def get_key(self):
        return f"{self.x}_{self.y}_{self.z}"

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        return self.x == other.x and \
               self.y == other.y and \
               self.z == other.z

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y, self.z - other.z)

    @property
    def l1(self):
        return abs(self.x) + abs(self.y) + abs(self.z)
    
    @property
    def l2(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)