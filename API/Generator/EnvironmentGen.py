from typing import List

from Simulator import Coordinate4D, Environment
from .MapTile import MapTile


class EnvironmentGen:

    def __init__(self, dimensions: "Coordinate4D", maptiles: List["MapTile"], allocation_period: int, min_height: int):
        self.dimensions = dimensions
        self.maptiles = maptiles
        self.min_height = min_height
        self.allocation_period = allocation_period

    def generate(self) -> "Environment":
        blockers = []
        for tile in self.maptiles:
            blockers += tile.resolve_buildings()
        env = Environment(self.dimensions, blockers, allocation_period=self.allocation_period,
                          min_height=self.min_height)
        return env
