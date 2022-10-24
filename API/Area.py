import math
from typing import List, TYPE_CHECKING, Union

from haversine import Direction, Unit, haversine, inverse_haversine

from Simulator import Coordinate2D, Coordinate3D
from .LongLatCoordinate import LongLatCoordinate

if TYPE_CHECKING:
    from .Types import APIWorldCoordinates, APIWeightedCoordinate

EARTH_RADIUS = 6371008.8


class Area:
    """
    Wrapper for field bounds defined by the bottom-left coordinate (in long-lat) and top-right coordinate (in long-lat)
    and the grid size in meters
    """

    def __init__(self, bottom_left_ll: Union["APIWorldCoordinates", "LongLatCoordinate"],
                 top_right_ll: Union["APIWorldCoordinates", "LongLatCoordinate"],
                 resolution: int = 1,
                 min_height: int = 0):
        self.bottom_left = LongLatCoordinate(bottom_left_ll.long, bottom_left_ll.lat)
        self.top_right = LongLatCoordinate(top_right_ll.long, top_right_ll.lat)
        self.resolution = resolution
        self.min_height = min_height // resolution

    def __repr__(self):
        return f"Area<tr={self.top_right}, bl={self.bottom_left}, r={self.resolution}>"

    @property
    def dimension(self):
        return self.lon_lat_to_grid(self.top_right)

    def lon_lat_to_grid(self, coords) -> List[float]:
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

    def point_to_coordinate2D(self, point: Union["LongLatCoordinate", "APIWeightedCoordinate"]):
        """
        Converts coordinates from longitude / latitude to our own "grid" Coordinate2D. Resulting coordinates
        are integer that can be negative.
        :param point: LongLatCoordinate | APIWeightedCoordinate - coordinate to be converted
        :return: Coordinate2D - converted point
        """
        x, y = self.lon_lat_to_grid(point)
        return Coordinate2D(math.floor(x), math.floor(y))

    def point_to_coordinate3D(self, point: Union["LongLatCoordinate", "APIWeightedCoordinate"], y: int):
        """
        Converts coordinates from longitude / latitude to our own "grid" Coordinate3D. Resulting coordinates
        are integer that can be negative.
        :param point: LongLatCoordinate | APIWeightedCoordinate - coordinate to be converted
        :param y: int - y coordinate of resulting coordinate 3D
        :return: Coordinate2D - converted point
        """
        coord2d = self.point_to_coordinate2D(point)
        return Coordinate3D(x=coord2d.x, y=y, z=coord2d.z)

    @staticmethod
    def haversin_lon_lat(bottom_left: "LongLatCoordinate", pos: "LongLatCoordinate"):
        """
        Calculates distance (delta-x, delta-y) in meters from bottom_left to pos
        :param bottom_left: LongLatCoordinate - origin of the playingfield in long/lat degrees
        :param pos: LongLatCoordinate - coordinate to be converted
        :return: (delta_x, delta_y) - distances along axis
        """
        delta_x = haversine((bottom_left.lat, bottom_left.long), (bottom_left.lat, pos.long), unit=Unit.METERS)
        delta_y = haversine((bottom_left.lat, bottom_left.long), (pos.lat, bottom_left.long), unit=Unit.METERS)

        if pos.long < bottom_left.long:
            delta_x *= -1
        if pos.lat < bottom_left.lat:
            delta_y *= -1
        return delta_x, delta_y

    @staticmethod
    def LCS_to_long_lat(bottom_left: "LongLatCoordinate", pos: "Coordinate2D", resolution: int) -> "LongLatCoordinate":
        """
        Calculates GCS from LCS
        :param bottom_left:
        :param pos:
        :param resolution:
        :return:
        """
        lat_corrected = inverse_haversine((bottom_left.lat, bottom_left.long), pos.z * resolution, Direction.NORTH,
                                          unit=Unit.METERS)[0]
        lat_long_corrected = inverse_haversine((lat_corrected, bottom_left.long), pos.x * resolution, Direction.EAST,
                                               unit=Unit.METERS)
        return LongLatCoordinate(lat_long_corrected[1], lat_long_corrected[0])
