from .Coordinate4D import Coordinate4D


class SaveCoordinate4D(Coordinate4D):

    def __init__(self, x: int, y: int, z: int, t: int, dimensions: Coordinate4D):
        self.__dimensions: Coordinate4D = dimensions
        super().__init__(self.save_x(x), self.save_y(y), self.save_z(z), self.save_t(t))

    def save_coord(self, attr, dim):
        min_attr = 0
        max_attr = getattr(self.__dimensions, dim)
        return min(max(attr, min_attr), max_attr - 1)

    def save_x(self, x):
        return self.save_coord(x, "x")

    def save_y(self, y):
        return self.save_coord(y, "y")

    def save_z(self, z):
        return self.save_coord(z, "z")

    def save_t(self, t):
        return self.save_coord(t, "t")

    def to_valid_coordinate(self):
        self.x = self.save_x(self.x)
        self.y = self.save_y(self.y)
        self.z = self.save_z(self.z)
        self.t = self.save_t(self.t)

    def __add__(self, other):
        super().__add__(other)
        self.to_valid_coordinate()

    def __sub__(self, other):
        super().__sub__(other)
        self.to_valid_coordinate()

    def random_neighbor(self, delta_t=0, chance_x=1/3, chance_y=1/3, chance_forward=0.5):
        time_coordinate = super().random_neighbor(delta_t=delta_t, chance_x=chance_x, chance_y=chance_y, chance_forward=chance_forward)
        return SaveCoordinate4D.from_time_coordinate(time_coordinate, self.__dimensions)

    @staticmethod
    def from_time_coordinate(time_coordinate: Coordinate4D, dimensions: Coordinate4D):
        return SaveCoordinate4D(
            time_coordinate.x, time_coordinate.y, time_coordinate.z, time_coordinate.t,
            dimensions=dimensions,
        )

