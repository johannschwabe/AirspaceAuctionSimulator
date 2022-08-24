from typing import List, TYPE_CHECKING

import cloudscraper

from Simulator import Coordinate4D, BuildingBlocker

if TYPE_CHECKING:
    from ..API import APIWorldCoordinates
    from ..Area import Area
    from .LongLatCoordinate import LongLatCoordinate


class MapTile:
    """
    A single osmbuildings tile
    Defined by tile coordinates by which all buildings within this tile can be requested
    """
    def __init__(
        self,
        tile_ids: List[int],
        dimensions: "Coordinate4D",
        top_left_coordinate: "APIWorldCoordinates",
        bottom_right_coordinate: "APIWorldCoordinates",
        area: "Area"
    ):
        """
        :param tile_ids: int[3] - coordinates of the tile (In the tile-coordinate system)
        :param area: Area - field bounds and resolution
        """
        self.blockers = []
        self.z = tile_ids[0]
        self.x = tile_ids[1]
        self.y = tile_ids[2]
        self.area = area

    @property
    def url(self):
        return f"https://a.data.osmbuildings.org/0.2/anonymous/tile/{self.z}/{self.x}/{self.y}.json"

    def resolve_buildings(self):
        """
        Extract building information from tile and convert them to building blockers
        :return: BuildingBlocker[]
        """
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
                    translated_coords = self.area.lon_lat_to_grid(LongLatCoordinate(coord[0], coord[1]))

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
                        [self.area.lon_lat_to_grid(LongLatCoordinate(hole_coord[0], hole_coord[1]))
                         for hole_coord in hole])

                bounds = [Coordinate3D(min_x, 0, min_z),
                          Coordinate3D(max_x, building['properties']['height'] / self.area.resolution, max_z)]

                dimension = self.area.dimension
                if dimension[0] < min_x or \
                    dimension[1] < min_z or \
                    max_x < 0 or max_z < 0:
                    continue
                new_blocker = BuildingBlocker(coords, bounds, holes)
                res.append(new_blocker)

        self.blockers = res
        return res

    def __str__(self):
        return f"x:{self.x}, y:{self.y}, z:{self.z}"
