from ..Coordinate import Coordinate
from ..IO import Stringify


class Blocker(Stringify):

    def __init__(self, origin: Coordinate, dimension: Coordinate):
        self.origin: Coordinate = origin
        self.dimension: Coordinate = dimension
