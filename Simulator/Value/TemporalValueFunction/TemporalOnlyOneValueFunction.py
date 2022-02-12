from ..OnlyOneValueFunction import OnlyOneValueFunction
from ...Time import Tick


class TemporalOnlyOneValue(OnlyOneValueFunction):
    def __init__(self, optimum: Tick):
        super().__init__(optimum)
