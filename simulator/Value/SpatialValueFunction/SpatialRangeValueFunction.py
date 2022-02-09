from .SpatialDifferenceFunction import SpatialDifferenceFunction
from ..RangeValueFunction import RangeValueFunction
from ...Coordinates.Coordinate import Coordinate


class SpatialRangeValueFunction(SpatialDifferenceFunction, RangeValueFunction):
    def __init__(self, optimum: Coordinate, equi_valuable_range: Coordinate, norm="l1"):
        super().__init__(norm=norm)
        super().__init__(optimum=optimum, equi_valuable_range=equi_valuable_range)
        self.norm = norm

