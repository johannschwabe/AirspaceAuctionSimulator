from typing import List, TYPE_CHECKING

from ..Blocker import Blocker
from ..Coordinate import Coordinate4D

if TYPE_CHECKING:
    from .MapTile import MapTile


class BlockerGen:

    def __init__(self, dimension: Coordinate4D, maptiles: List["MapTile"]):
        self.dimension: Coordinate4D = dimension
        self.maptiles: List["MapTile"] = maptiles

    def generate_maptile_blockers(self):
        blockers: List[Blocker] = []
        for tile in self.maptiles:
            blockers += tile.resolve_buildings()
        return blockers

    def generate(self, n_blockers: int):
        blockers: List[Blocker] = []
        max_size = Coordinate(
            int(self.dimension.x / 5),
            int(self.dimension.y),
            int(self.dimension.z / 5),
        )
        for _ in range(n_blockers):
            origin = Coordinate.random(self.dimension)
            origin.y = 0
            dimension = Coordinate.random(max_size, strict_positive=True)
            locations: List[Coordinate4D] = \
                [Coordinate4D(origin.x, origin.y, origin.z, t)) for t in range(self.dimension.t + 1)]
            blockers.append(Blocker(locations, dimension))
        return blockers
