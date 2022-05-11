from typing import List, TYPE_CHECKING

import requests

from Simulator.Coordinate import TimeCoordinate

if TYPE_CHECKING:
    from API import SimpleCoordinateType


class MapTile:

    def __init__(
        self,
        tile_ids: List[int],
        dimensions: TimeCoordinate,
        top_left_coordinate: "SimpleCoordinateType",
        bottom_right_coordinate: "SimpleCoordinateType",
    ):
        self.z = tile_ids[0]
        self.x = tile_ids[1]
        self.y = tile_ids[2]
        self.dimensions = dimensions
        self.top_left_coordinate = top_left_coordinate
        self.bottom_right_coordinate = bottom_right_coordinate

    @property
    def url(self):
        return f"https://a.data.osmbuildings.org/0.2/anonymous/tile/{self.z}/{self.x}/{self.y}.json"

    def resolve_buildings(self):
        data = requests.get(self.url).json()
        print("***OSM***", data)
