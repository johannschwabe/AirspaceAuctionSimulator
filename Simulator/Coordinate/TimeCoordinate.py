from .Coordinate import Coordinate
from ..Time import Tick


class TimeCoordinate(Coordinate):

    def __init__(self, x: int, y: int, z: int, t: Tick):
        super().__init__(x, y, z)
        self.t: Tick = t

    def get_key(self):
        return f"{self.x}_{self.y}_{self.z}_{self.t}"

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z}, {self.t})"

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z}, {self.t})"

    def __eq__(self, other):
        return self.x == other.x and \
               self.y == other.y and \
               self.z == other.z and \
               self.t == other.t

    def inter_temporal_equal(self, other):
        return super().__eq__(other)

    def to_inter_temporal(self):
        return Coordinate(self.x, self.y, self.z)

    def __add__(self, other):
        t_other = 0
        if type(other).__name__ == "TimeCoordinates":
            t_other = other.t
        return TimeCoordinate(self.x + other.x, self.y + other.y, self.z + other.z, self.t + t_other)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y, self.z - other.z)

    def distance(self, other, l2: bool = False):
        temp = 0
        if isinstance(other, TimeCoordinate):
            temp = abs(self.t - other.t)
        return super().distance(other, l2), temp

    def inter_temporal_distance(self, other: Coordinate, l2: bool = False):
        return super().distance(other, l2)

    def clone(self):
        return TimeCoordinate(self.x, self.y, self.z, self.t)
