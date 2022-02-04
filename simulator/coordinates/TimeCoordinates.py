from Coordinates import Coordinates


class TimeCoordinates(Coordinates):

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

    def inter_temporal_equal(self, other):
        return self.x == other.x and \
               self.y == other.y and \
               self.z == other.z

    def to_inter_temporal(self):
        return Coordinates(self.x, self.y, self.z)

    def __add__(self, other):
        t_other = 0
        if type(other).__name__ == "TimeCoordinates":
            t_other = other.t
        return TimeCoordinates(self.x + other.x, self.y + other.y, self.z + other.z, self.t + t_other)

    def __sub__(self, other):
        return Coordinates(self.x - other.x, self.y - other.y, self.z - other.z)