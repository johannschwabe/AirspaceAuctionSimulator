from typing import List
from .BlockerGen import Blocker, BlockerGen
from ..Environment import Environment
from ..Coordinate import TimeCoordinate, Coordinate


class EnvironmentGen:

    def __init__(self, dimensions: TimeCoordinate):
        self.dimensions: TimeCoordinate = dimensions

    def generate(self, n_blockers: int) -> Environment:
        blockers: List[Blocker] = BlockerGen(self.dimensions).generate(n_blockers)
        return Environment(self.dimensions, blockers)
