from typing import List, TYPE_CHECKING

from ..Blocker import Blocker
from ..Coordinate import Coordinate, TimeCoordinate
from ..Time import Tick

if TYPE_CHECKING:
    from .MapTile import MapTile


class BlockerGen:

    def __init__(self, dimension: TimeCoordinate, maptiles: List["MapTile"]):
        self.dimension: TimeCoordinate = dimension
        self.maptiles: List["MapTile"] = maptiles

    def generate(self, n_blockers: int):
        # TODO generate according to maptiles!
        blockers: List[Blocker] = []
        max_size = Coordinate(
            int(self.dimension.x / 5),
            int(self.dimension.y / 2),
            int(self.dimension.z / 10),
        )
        for i in range(n_blockers):
            origin = Coordinate.random(self.dimension)
            origin.y = 0
            dimension = Coordinate.random(max_size)
            locations: List[TimeCoordinate] = \
                [TimeCoordinate(origin.x + i, origin.y, origin.z, Tick(t)) for i, t in enumerate(range(self.dimension.t + 1))]
            blockers.append(Blocker(locations, dimension))
        return blockers
