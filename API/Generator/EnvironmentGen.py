from typing import List, Optional, TYPE_CHECKING

from Simulator import Environment

if TYPE_CHECKING:
    from Simulator.Blocker.Blocker import Blocker
    from Simulator import Coordinate4D
    from .MapTile import MapTile
    from API.Area import Area


class EnvironmentGen:

    def __init__(self,
                 dimensions: "Coordinate4D",
                 maptiles: List["MapTile"],
                 map_area: "Area",
                 blockers: Optional[List["Blocker"]] = None
                 ):
        self.dimensions = dimensions
        self.maptiles = maptiles
        self.map_area = map_area
        self.blockers = [] if blockers is None else blockers

    def generate(self) -> "Environment":
        blockers = [*self.blockers]
        for tile in self.maptiles:
            blockers += tile.resolve_buildings(self.map_area)
        env = Environment(self.dimensions, blockers, min_height=self.map_area.min_height)
        return env
