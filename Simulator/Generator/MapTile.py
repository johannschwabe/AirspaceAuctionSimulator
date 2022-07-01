import cloudscraper
from typing import List, TYPE_CHECKING

from Simulator.Blocker.BuildingBlocker import BuildingBlocker
from Simulator.Coordinate import Coordinate4D

if TYPE_CHECKING:
    from API import SimpleCoordinateType


class MapTile:

    def __init__(
        self,
        tile_ids: List[int],
        dimensions: Coordinate4D,
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
        data = cloudscraper.create_scraper().get(self.url).json()
        res = []
        for building in data["features"]:
            is_feature = building["type"] == 'Feature'
            has_height = building['properties']['height'] > 0
            is_polygon = building['geometry']['type'] == 'Polygon'
            has_coordinates = (
                len(building['geometry']['coordinates']) > 0 and len(building['geometry']['coordinates'][0]) > 0
            )
            if is_feature and has_height and is_polygon and has_coordinates:
                coords = []
                min_x = 100000
                max_x = -100000
                min_z = 100000
                max_z = -100000
                for coord in building['geometry']['coordinates'][0]:
                    z = (
                            (coord[0] - self.top_left_coordinate.long) /
                            (self.bottom_right_coordinate.long - self.top_left_coordinate.long)
                        ) * self.dimensions.x
                    x = (
                            (coord[1] - self.top_left_coordinate.lat) /
                            (self.bottom_right_coordinate.lat - self.top_left_coordinate.lat)
                        ) * self.dimensions.z
                    coords.append([x, z])

                    if min_x > x:
                        min_x = x
                    if min_z > z:
                        min_z = z
                    if max_x < x:
                        max_x = x
                    if max_z < z:
                        max_z = z
                bounds = [Coordinate4D(min_x, 0, min_z, 0),
                          Coordinate4D(max_x, building['properties']['height'], max_z, self.dimensions.t * 10000)]
                new_blocker = BuildingBlocker(coords, bounds)
                res.append(new_blocker)

        return res

    def __str__(self):
        return f"x:{self.x}, y:{self.y}, z:{self.z}"
