from ..OnlyOneValueFunction import OnlyOneValueFunction
from ...Coordinates import Coordinate


class SpatialOnlyOneValue(OnlyOneValueFunction):
    def __init__(self, optimum: Coordinate):
        super().__init__(optimum)
