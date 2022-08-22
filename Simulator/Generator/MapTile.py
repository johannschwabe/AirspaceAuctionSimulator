import cloudscraper
from typing import List, TYPE_CHECKING

from CoordinateTransformations import lon_lat_to_grid
from Simulator.Blocker.BuildingBlocker import BuildingBlocker
from Simulator.Coordinate import Coordinate4D

if TYPE_CHECKING:
    from Simulator.Generator.Area import Area


class MapTile:

    def __init__(
        self,
        tile_ids: List[int],
        dimensions: Coordinate4D,
        area: "Area"
    ):
        self.blockers = []
        self.z = tile_ids[0]
        self.x = tile_ids[1]
        self.y = tile_ids[2]
        self.dimensions = dimensions
        self.area = area

    @property
    def url(self):
        return f"https://a.data.osmbuildings.org/0.2/anonymous/tile/{self.z}/{self.x}/{self.y}.json"

    def is_in_subselection(self, coordinate):
        return self.area.bottom_left.long < coordinate[0] < self.area.top_right.long and \
               self.area.bottom_left.lat < coordinate[1] < self.area.top_right.lat

    def resolve_buildings(self):
        if len(self.blockers) > 0:
            return self.blockers
        raw_data = cloudscraper.create_scraper().get(self.url)
        if raw_data.status_code != 200:
            print(raw_data.status_code)
            return []
        data = raw_data.json()
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
                holes = []
                min_x = 100000
                max_x = -100000
                min_z = 100000
                max_z = -100000
                for coord in building['geometry']['coordinates'][0]:
                    translated_coords = lon_lat_to_grid([self.area.bottom_left.long,
                                                         self.area.bottom_left.lat],
                                                        self.area.resolution, coord)
                    coords.append(translated_coords)
                    x = translated_coords[0]
                    z = translated_coords[1]
                    if min_x > x:
                        min_x = x
                    if min_z > z:
                        min_z = z
                    if max_x < x:
                        max_x = x
                    if max_z < z:
                        max_z = z
                for hole in building['geometry']['coordinates'][1:]:
                    holes.append(
                        [lon_lat_to_grid([self.area.bottom_left.long,
                                          self.area.bottom_left.lat],
                                         self.area.resolution, hole_coord) for hole_coord in hole])

                bounds = [Coordinate4D(min_x, 0, min_z, 0),
                          Coordinate4D(max_x, building['properties']['height'], max_z,
                                       self.dimensions.t + 1000)]  # Todo remove magic number 1000

                top_right_grid = lon_lat_to_grid([self.area.bottom_left.long,
                                                  self.area.bottom_left.lat],
                                                 self.area.resolution,
                                                 [self.area.top_right.long,
                                                  self.area.top_right.lat])
                if min_x > top_right_grid[0] > 0 or \
                    min_x > top_right_grid[1] > 0 or \
                    max_x < 0 or max_z < 0:
                    continue
                new_blocker = BuildingBlocker(coords, bounds, holes)
                res.append(new_blocker)

        self.blockers = res
        return res

    def __str__(self):
        return f"x:{self.x}, y:{self.y}, z:{self.z}"
