from typing import List, TYPE_CHECKING, Tuple

import requests
import mpmath as mp

from API.Area import Area
from API.LongLatCoordinate import LongLatCoordinate
from Simulator import BuildingBlocker, Coordinate3D

if TYPE_CHECKING:
    from API.Types import APIWorldCoordinates

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
DEFAULT_BUILDING_HEIGHT_M = 10
METERS_PER_LEVEL = 3


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
    def overpass_query(self) -> str:
        s = self.area.bottom_left.lat
        w = self.area.bottom_left.long
        n = self.area.top_right.lat
        e = self.area.top_right.long
        return (
            f"[out:json][timeout:30];"
            f"(way[\"building\"]({s},{w},{n},{e});"
            f"relation[\"building\"][\"type\"=\"multipolygon\"]({s},{w},{n},{e}););"
            f"out geom;"
        )

    @staticmethod
    def _parse_height(tags: dict) -> float:
        if tags.get("height"):
            try:
                h = float(tags["height"])
                if h > 0:
                    return h
            except (ValueError, TypeError):
                pass
        if tags.get("building:levels"):
            try:
                levels = float(tags["building:levels"])
                if levels > 0:
                    return levels * METERS_PER_LEVEL
            except (ValueError, TypeError):
                pass
        return DEFAULT_BUILDING_HEIGHT_M

    def _geom_to_grid(self, geom: list, map_playfield_area: Area) -> list:
        return [
            map_playfield_area.lon_lat_to_grid(LongLatCoordinate(pt["lon"], pt["lat"]))
            for pt in geom
            if "lat" in pt and "lon" in pt
        ]

    def _build_blocker(self, coords: list, holes: list, height_m: float,
                       map_playfield_area: Area, element_id: int):
        if len(coords) < 3:
            return None
        min_x = min(c[0] for c in coords)
        max_x = max(c[0] for c in coords)
        min_z = min(c[1] for c in coords)
        max_z = max(c[1] for c in coords)
        height_grid = height_m / map_playfield_area.resolution
        bounds = [Coordinate3D(min_x, 0, min_z), Coordinate3D(max_x, height_grid, max_z)]
        dimension = map_playfield_area.dimension
        if dimension[0] < min_x or dimension[1] < min_z or max_x < 0 or max_z < 0:
            return None
        return BuildingBlocker(coords, bounds, holes, element_id)

    def resolve_buildings(self, map_playfield_area: Area):
        """
        Extract building information via Overpass API and convert to building blockers.
        :return: BuildingBlocker[]
        """
        if len(self.blockers) > 0:
            return self.blockers
        try:
            resp = requests.post(
                OVERPASS_URL,
                data={"data": self.overpass_query},
                timeout=35,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"Overpass API error: {e}")
            return []

        res = []
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            height_m = self._parse_height(tags)
            element_id = element.get("id", 0)

            if element["type"] == "way":
                geom = element.get("geometry", [])
                coords = self._geom_to_grid(geom, map_playfield_area)
                blocker = self._build_blocker(coords, [], height_m, map_playfield_area, element_id)

            elif element["type"] == "relation":
                members = element.get("members", [])
                outers = [m for m in members if m.get("role") == "outer" and m.get("geometry")]
                inners = [m for m in members if m.get("role") == "inner" and m.get("geometry")]
                if not outers:
                    continue
                coords = self._geom_to_grid(outers[0]["geometry"], map_playfield_area)
                holes = [self._geom_to_grid(m["geometry"], map_playfield_area) for m in inners]
                blocker = self._build_blocker(coords, holes, height_m, map_playfield_area, element_id)

            else:
                continue

            if blocker is not None:
                res.append(blocker)

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
