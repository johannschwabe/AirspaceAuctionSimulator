from typing import List

from Simulator import Coordinate4D, Environment
from .MapTile import MapTile
from ..Area import Area


class EnvironmentGen:

    def __init__(self, dimensions: "Coordinate4D", maptiles: List["MapTile"], map_playfield_area: Area, allocation_period: int, min_height: int):
        self.dimensions = dimensions
        self.maptiles = maptiles
        self.allocation_period = allocation_period
        self.map_playfield_area = map_playfield_area
        self.min_height = min_height

    def generate(self) -> "Environment":
        blockers = []
        for tile in self.maptiles:
            blockers += tile.resolve_buildings(self.map_playfield_area)
        env = Environment(self.dimensions, blockers, allocation_period=self.allocation_period,
                          min_height=self.min_height)
        return env
