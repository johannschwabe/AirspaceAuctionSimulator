import math
from typing import TYPE_CHECKING

from Simulator import Coordinate2D
from .LongLatCoordinate import LongLatCoordinate

if TYPE_CHECKING:
    from .API import APIWorldCoordinates

EARTH_RADIUS = 6371008.8


class Area:
    """
    Wrapper for field bounds defined by the bottom-left coordinate (in long-lat) and top-right coordinate (in long-lat)
    and the grid size in meters
    """

    def __init__(self, bottom_left_ll: "APIWorldCoordinates", top_right_ll: "APIWorldCoordinates", resolution: int,
                 min_height: int = 0):
        self.bottom_left = LongLatCoordinate(bottom_left_ll.long, bottom_left_ll.lat)
        self.top_right = LongLatCoordinate(top_right_ll.long, top_right_ll.lat)
        self.resolution = resolution
        self.min_height = min_height

    def __repr__(self):
        return f"Area<tr={self.top_right}, bl={self.bottom_left}, r={self.resolution}>"

    @property
    def dimension(self):
        return self.lon_lat_to_grid(self.top_right)

    def lon_lat_to_grid(self, coords):
        """
        Converts coordinates from longitude / latitude to our own "grid" coordinates. Resulting coordinates
        are floats that can be negative.
        :param coords: LongLatCoordinate - coordinate to be converted
        :return: (long, lat) - converted coords
        """
        coords_m = self.haversin_lon_lat(self.bottom_left, coords)
        x = coords_m[0] / self.resolution
        z = coords_m[1] / self.resolution
        return [x, z]

    def point_to_coordinate2D(self, point: "LongLatCoordinate | APIWeightedCoordinate"):
        """
        Converts coordinates from longitude / latitude to our own "grid" Coordinate2D. Resulting coordinates
        are integer that can be negative.
        :param point: LongLatCoordinate | APIWeightedCoordinate - coordinate to be converted
        :return: Coordinate2D - converted point
        """
        x, y = self.lon_lat_to_grid(point)
        return Coordinate2D(math.floor(x), math.floor(y))

    @staticmethod
    def haversin_lon_lat(bottom_left: "LongLatCoordinate", pos):
        """
        Calculates distance (delta-x, delta-y) in meters from bottom_left to pos
        :param bottom_left: LongLatCoordinate - origin of the playingfield in long/lat degrees
        :param pos: LongLatCoordinate - coordinate to be converted
        :return: (delta_x, delta_y) - distances along axis
        """
        delta_x = 2 * EARTH_RADIUS * math.asin(math.sqrt(
            math.cos(math.radians(bottom_left.lat)) * math.cos(math.radians(pos.lat)) * math.sin(
                math.radians((pos.long - bottom_left.long) / 2)) ** 2))
        delta_y = 2 * EARTH_RADIUS * math.asin(math.sqrt(
            math.sin(
                math.radians((pos.lat - bottom_left.lat) / 2)) ** 2))
        if pos.long < bottom_left.long:
            delta_x *= -1
        if pos.lat < bottom_left.lat:
            delta_y *= -1
        return delta_x, delta_y
