from typing import List

from Simulator import Environment, Coordinate4D
from MapTile import MapTile


class EnvironmentGen:

    def __init__(self, dimensions: "Coordinate4D", maptiles: List["MapTile"]):
        self.dimensions = dimensions
        self.maptiles = maptiles

    def generate(self) -> "Environment":
        blockers = []
        for tile in self.maptiles:
            blockers += tile.resolve_buildings()
        env = Environment.init(self.dimensions, blockers)
        return env
