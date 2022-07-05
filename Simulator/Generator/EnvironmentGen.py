from typing import List, TYPE_CHECKING

from .BlockerGen import Blocker, BlockerGen
from ..Environment import Environment
from ..Coordinate import Coordinate4D, Coordinate3D

if TYPE_CHECKING:
    from .MapTile import MapTile


class EnvironmentGen:

    def __init__(self, dimensions: Coordinate4D, maptiles: List["MapTile"]):
        self.dimensions: Coordinate4D = dimensions
        self.maptiles: List["MapTile"] = maptiles

    def generate(self, n_blockers: int) -> Environment:
        blockers: List[Blocker] = BlockerGen(self.dimensions, self.maptiles).generate_maptile_blockers()
        env = Environment(self.dimensions, blockers, self.maptiles)
        return env
