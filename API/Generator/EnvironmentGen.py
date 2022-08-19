from typing import List

from MapTile import MapTile
from Simulator import Environment, Coordinate4D


class EnvironmentGen:

    def __init__(self, dimensions: "Coordinate4D", maptiles: List["MapTile"]):
        self.dimensions = dimensions
        self.maptiles = maptiles

    def generate(self) -> "Environment":
        blockers = []
        for tile in self.maptiles:
            blockers += tile.resolve_buildings()
        env = Environment(self.dimensions, blockers)
        return env
