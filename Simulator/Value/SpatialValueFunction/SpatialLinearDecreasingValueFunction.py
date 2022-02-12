from .SpatialDifferenceFunction import SpatialDifferenceFunction
from ..LinearDecreasingValueFunction import LinearDecreasingValueFunction
from ...Coordinate import Coordinate


class SpatialLinearDecreasingValue(SpatialDifferenceFunction, LinearDecreasingValueFunction):

    def __init__(self, optimum: Coordinate, distance_to_zero: float, norm="l1"):
        super().__init__(norm=norm)
        super().__init__(optimum=optimum, distance_to_zero=distance_to_zero)
