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
        for i in range(n_blockers):
            origin = Coordinate.random(self.dimension)
            origin.y = 0
            size = Coordinate.random(max_size)
            locations: List[TimeCoordinate] = \
                [TimeCoordinate(origin.x, origin.y, origin.z, Tick(t)) for t in range(self.dimension.t + 1)]
            blocked_coordinates: List[Coordinate] = []
            for x in range(size.x):
                for y in range(size.y):
                    for z in range(size.z):
                        blocked_coordinates.append(Coordinate(
                            origin.x + x,
                            origin.y + y,
                            origin.z + z
                        ))

            blockers.append(Blocker(locations, blocked_coordinates))
        return blockers
