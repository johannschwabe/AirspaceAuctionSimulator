from .ValueFunction import ValueFunction
from ..Time import Tick
from ..Coordinate import TimeCoordinate


def is_same(val_1, val_2) -> bool:        # Is that the idea of this function @Joel
    if isinstance(val_1, Tick) and isinstance(val_2, Tick):
        return val_1 == val_2
    return TimeCoordinate.inter_temporal_equal(val_1, val_2)


class OnlyOneValueFunction(ValueFunction):
    def __init__(self, optimum):
        super().__init__(optimum)

    def __call__(self, point_of_interest, **kwargs) -> float:
        if is_same(point_of_interest, self.optimum):
            return 1.0
        return 0.0
