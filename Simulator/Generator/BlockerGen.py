from typing import List

from ..Blocker import Blocker
from ..Coordinate import Coordinate, TimeCoordinate
from ..Time import Tick


class BlockerGen:

    def __init__(self, dimension: TimeCoordinate):
        self.dimension: TimeCoordinate = dimension

    def generate(self, n_blockers: int):
        blockers: List[Blocker] = []
        max_size = Coordinate(
            int(self.dimension.x / 5),
            int(self.dimension.y / 2),
            int(self.dimension.z / 10),
        )
        for _ in range(n_blockers):
            origin = Coordinate.random(self.dimension)
            origin.y = 0
            dimension = Coordinate.random(max_size)
            locations: List[TimeCoordinate] = \
                [TimeCoordinate(origin.x, origin.y, origin.z, Tick(t)) for t in range(self.dimension.t + 1)]
            blockers.append(Blocker(locations, dimension))
        return blockers
