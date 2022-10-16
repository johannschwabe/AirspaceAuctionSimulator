from typing import List, TYPE_CHECKING

from Simulator import Environment

if TYPE_CHECKING:
    from Simulator import Coordinate4D
    from .MapTile import MapTile
    from API.Area import Area


class EnvironmentGen:

    def __init__(self,
                 dimensions: "Coordinate4D",
                 maptiles: List["MapTile"],
                 map_area: "Area",
                 allocation_period: int,
                 min_height: int):
        self.dimensions = dimensions
        self.maptiles = maptiles
        self.allocation_period = allocation_period
        self.map_area = map_area
        self.min_height = min_height

    def generate(self) -> "Environment":
        blockers = []
        for tile in self.maptiles:
            blockers += tile.resolve_buildings(self.map_area)
        env = Environment(self.dimensions, blockers, allocation_period=self.allocation_period,
                          min_height=self.min_height)
        return env
