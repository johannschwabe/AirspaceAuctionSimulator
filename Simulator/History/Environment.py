from typing import List
from .Blocker import Blocker
from ..Coordinate import TimeCoordinate, Coordinate
from ..IO import Stringify


class Environment(Stringify):

    def __init__(self, dimensions: TimeCoordinate, n_blockers: int):
        self.dimensions: TimeCoordinate = dimensions
        self.blockers: List[Blocker] = []
        self.generate(n_blockers)

    def generate(self, n_blockers: int):
        max_size = Coordinate(
            int(self.dimensions.x / 5),
            int(self.dimensions.y / 2),
            int(self.dimensions.z / 10),
        )
        for i in range(n_blockers):
            origin = Coordinate.random(self.dimensions)
            origin.y = 0
            size = Coordinate.random(max_size)
            self.blockers.append(Blocker(origin, size))

