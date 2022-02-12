from ..OnlyOneValueFunction import OnlyOneValueFunction
from ...Coordinate import Coordinate


class SpatialOnlyOneValue(OnlyOneValueFunction):
    def __init__(self, optimum: Coordinate):
        super().__init__(optimum)
