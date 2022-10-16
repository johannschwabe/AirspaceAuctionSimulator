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
                 min_height: int):
        self.dimensions = dimensions
        self.maptiles = maptiles
        self.map_area = map_area
        self.min_height = min_height

    def generate(self) -> "Environment":
        blockers = []
        for tile in self.maptiles:
            blockers += tile.resolve_buildings(self.map_area)
        env = Environment(self.dimensions, blockers, min_height=self.min_height)
        return env
