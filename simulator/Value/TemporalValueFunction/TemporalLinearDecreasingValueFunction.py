from ..LinearDecreasingValueFunction import LinearDecreasingValueFunction
from ...Time.Tick import Tick


class TemporalLinearDecreasingValue(LinearDecreasingValueFunction):

    def __init__(self, optimum: Tick, distance_to_zero: Tick):
        super().__init__(optimum, distance_to_zero)

