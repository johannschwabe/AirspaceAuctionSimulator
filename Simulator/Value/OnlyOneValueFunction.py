from .ValueFunction import ValueFunction
from ..Coordinate import TimeCoordinate, Coordinate


class OnlyOneValueFunction(ValueFunction):
    def __init__(self, optimum):
        super().__init__(optimum)

    def __call__(self, point_of_interest, **kwargs) -> float:
        if self.is_same(point_of_interest, self.optimum):
            return 1.0
        return 0.0

    @staticmethod
    def is_same(val_1, val_2) -> bool:
        if (isinstance(val_1, TimeCoordinate) or isinstance(val_1, Coordinate)) and \
                (isinstance(val_2, TimeCoordinate) or isinstance(val_2, Coordinate)):
            return val_1.inter_temporal_equal(val_2)

        return val_1 == val_2
