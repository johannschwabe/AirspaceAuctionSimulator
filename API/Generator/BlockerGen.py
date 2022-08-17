from typing import List, TYPE_CHECKING

from AAS.Blocker import Blocker
from AAS.Coordinates import Coordinate4D, Coordinate3D

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
