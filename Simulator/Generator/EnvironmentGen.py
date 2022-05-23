from typing import List, TYPE_CHECKING

from .BlockerGen import Blocker, BlockerGen
from ..Environment import Environment
from ..Coordinate import TimeCoordinate, Coordinate

if TYPE_CHECKING:
    from .MapTile import MapTile


class EnvironmentGen:

    def __init__(self, dimensions: TimeCoordinate, maptiles: List["MapTile"]):
        self.dimensions: TimeCoordinate = dimensions
        self.maptiles: List["MapTile"] = maptiles

    def generate(self, n_blockers: int) -> Environment:
        blockers: List[Blocker] = BlockerGen(self.dimensions, self.maptiles).generate(n_blockers)
        env = Environment(self.dimensions, blockers, self.maptiles)
        env.set_blockers(blockers)
        return env
