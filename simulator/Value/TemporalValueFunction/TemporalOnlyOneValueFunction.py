from ..OnlyOneValueFunction import OnlyOneValueFunction
from ...Time.Tick import Tick


class TemporalOnlyOneValue(OnlyOneValueFunction):
    def __init__(self, optimum: Tick):
        super().__init__(optimum)

