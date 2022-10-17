from typing import List, TYPE_CHECKING, Tuple

import cloudscraper
import mpmath as mp

from API.Area import Area
from API.LongLatCoordinate import LongLatCoordinate
from Simulator import BuildingBlocker, Coordinate3D

if TYPE_CHECKING:
    from API.Types import APIWorldCoordinates


class MapTile:
    """
    A single osmbuildings tile
    Defined by tile coordinates by which all buildings within this tile can be requested
    """

    def __init__(
            self,
            tile_ids: List[int],
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

    def resolve_buildings(self, map_playfield_area: Area):
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
                    translated_coords = map_playfield_area.lon_lat_to_grid(LongLatCoordinate(coord[0], coord[1]))

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
                        [map_playfield_area.lon_lat_to_grid(LongLatCoordinate(hole_coord[0], hole_coord[1]))
                         for hole_coord in hole])

                bounds = [Coordinate3D(min_x, 0, min_z),
                          Coordinate3D(max_x, building['properties']['height'] / map_playfield_area.resolution, max_z)]

                dimension = map_playfield_area.dimension
                if dimension[0] < min_x or dimension[1] < min_z or max_x < 0 or max_z < 0:
                    continue
                new_blocker = BuildingBlocker(coords, bounds, holes, building["id"])
                res.append(new_blocker)

        self.blockers = res
        return res

    def __repr__(self):
        return f"x:{self.x}, y:{self.y}, z:{self.z}"

    @property
    def zxy(self):
        return [self.z, self.x, self.y]

    @property
    def long(self) -> float:
        """
        Returns the longitude of the top-left anchor point of the maptile
        :return: longitude
        """
        return MapTile.zxy2lon(self.z, self.x, self.y)

    @property
    def lat(self) -> float:
        """
        Returns the latitude of the top-left anchor point of the maptile
        :return: latitude
        """
        return MapTile.zxy2lon(self.z, self.x, self.y)

    @property
    def coordinates(self) -> LongLatCoordinate:
        """
        Returns the longitude latitude of the top-left anchor point of the maptile
        :return: LongLatCoordinate
        """
        return LongLatCoordinate(long=self.long, lat=self.lat)

    @property
    def bottom_left_coordinate(self) -> LongLatCoordinate:
        """
        Returns the longitude latitude of the bottom-left point of the maptile
        This is usually the origin of our simulation world
        :return:
        """
        return self.area.bottom_left

    @property
    def top_right_coordinate(self) -> LongLatCoordinate:
        """
        Returns the longitude latitude of the top-right point of the maptile
        This point usually spans the playing field from the origin in our simulations
        :return:
        """
        return self.area.top_right

    @staticmethod
    def zxy2lon(z: int, x: int, y: int) -> float:
        """
        Converts a raw maptile definition using z,x,y to the longitude of its anchor point at the top-left
        Source: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Tile_numbers_to_lon./lat._2
        :param z: Zoom
        :param x: horizontal index
        :param y: vertical index
        :return: longitude
        """
        n = 2.0 ** z
        lon = x / n * 360.0 - 180.0
        return lon

    @staticmethod
    def zxy2lat(z: int, x: int, y: int) -> float:
        """
        Converts a raw maptile definition using z,x,y to the latitude of its anchor point at the top-left
        Source: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Tile_numbers_to_lon./lat._2
        :param z: Zoom
        :param x: horizontal index
        :param y: vertical index
        :return: latitude
        """
        n = 2.0 ** z
        lat_rad = mp.atan(mp.sinh(mp.pi * (1 - 2 * y / n)))
        lat = mp.degrees(lat_rad)
        return float(lat)

    @staticmethod
    def tiles_from_coordinates(coordinates: "APIWorldCoordinates",
                               neighbouring_tiles: int = 0,
                               resolution: int = 1) -> List["MapTile"]:
        """
        Given an input coordinate, returns a list of MapTiles centering that coordinate, including neighbouring
        maptiles according to the input parameters
        Source: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon./lat._to_tile_numbers_2
        :param coordinates: Coordinate that will be covered by the maptile at the center of the array
        :param neighbouring_tiles:
        :param resolution:
        :return: Array of maptiles, starting from the top-left tile, left-to-right, top-to-bottom flow: [[1,2,3], [4,
        5, 6], [7, 8, 9]]
                 The number of tiles returned is always (1 + (neighbouring_tiles * 2)^2
                 Hence: 0->1, 1->9, 2->25 etc.
        """
        lat_rad = mp.radians(coordinates.lat)
        n = 2 ** 15

        xtile = int((coordinates.long + 180.0) / 360.0 * n)
        ytile = int((1.0 - mp.asinh(mp.tan(lat_rad)) / mp.pi) / 2.0 * n)

        tiles = []
        for i in range(-neighbouring_tiles, neighbouring_tiles + 1):
            for j in range(-neighbouring_tiles, neighbouring_tiles + 1):
                z, x, y = 15, xtile + j, ytile + i
                tile_ids = [z, x, y]
                bottom_left, top_right = MapTile.bounding_box_from_zxy(z, x, y)
                area = Area(bottom_left, top_right, resolution)
                tiles.append(MapTile(tile_ids=tile_ids, area=area))
        return tiles

    @staticmethod
    def bounding_box_from_zxy(z: int, x: int, y: int) -> Tuple[LongLatCoordinate, LongLatCoordinate]:
        """
        Returns the bounding box of a MapTile given in raw z,x,y format. The bounding box spans a field
        from the bottom-left coordinate to the top-right coordiante
        :param z: Zoom
        :param x: horizontal index
        :param y: vertical index
        :return: Bottom-Left LongLatCoordinate, Top-Right LongLatCoordinate
        """
        bottom_left_lat = MapTile.zxy2lat(z, x, y + 1)
        bottom_left_lon = MapTile.zxy2lon(z, x, y + 1)

        top_right_lat = MapTile.zxy2lat(z, x + 1, y)
        top_right_lon = MapTile.zxy2lon(z, x + 1, y)

        bottom_left = LongLatCoordinate(lat=bottom_left_lat, long=bottom_left_lon)
        top_right = LongLatCoordinate(lat=top_right_lat, long=top_right_lon)

        return bottom_left, top_right

    @staticmethod
    def bounding_box_from_maptiles_group(maptiles: List["MapTile"]) -> Tuple[LongLatCoordinate, LongLatCoordinate]:
        """
        Returns the bounding box of a group of MapTiles that form a squared grid. Hence, the number of input maptiles
        must be the square root of an uneven number (1, 9, 25...), starting with the maptile at the top left,
        flowing left-to-right and top-to-bottom. The bounding box is defined by the overall bottom-left and top-right
        coordinates of the maptile group
        :param maptiles: List of maptiles
        :return: Bottom-Left LongLatCoordinate, Top-Right LongLatCoordinate
        """
        n = len(maptiles)
        top_right_tile_index = int(mp.sqrt(n) - 1)
        top_right_tile = maptiles[top_right_tile_index]

        bottom_left_tile_index = int(n - mp.sqrt(n))
        bottom_left_tile = maptiles[bottom_left_tile_index]

        return bottom_left_tile.bottom_left_coordinate, top_right_tile.top_right_coordinate
