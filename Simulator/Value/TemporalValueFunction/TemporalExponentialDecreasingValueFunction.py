from ..ExponentialDecreasingValueFunction import ExponentialDecreasingValueFunction
from ...Time import Tick


class TemporalExponentialDecreasingValue(ExponentialDecreasingValueFunction):

    def __init__(self, optimum: Tick, distance_to_zero: Tick):
        super().__init__(optimum, distance_to_zero)
