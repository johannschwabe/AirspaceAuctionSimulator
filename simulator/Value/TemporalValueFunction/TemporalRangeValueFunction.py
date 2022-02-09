from ..RangeValueFunction import RangeValueFunction
from ...Time import Tick


class TemporalRangeValueFunction(RangeValueFunction):

    def __init__(self, optimum: Tick, equi_valuable_range: Tick):
        super().__init__(optimum, equi_valuable_range)

