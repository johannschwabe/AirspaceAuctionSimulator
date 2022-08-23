import math
from typing import TYPE_CHECKING

EARTH_RADIUS = 6371008.8
from Simulator.Coordinate import Coordinate2D

if TYPE_CHECKING:
    from API import APIWeightedCoordinate
    from Simulator.Generator.Area import LongLatCoordinate, Area


def haversin_lon_lat(bottom_left: "LongLatCoordinate", pos):
    """
    Calculates distance (delta-x, delta-y) in meters from bottom_left to pos
    :param bottom_left: LongLatCoordinate - origin of the playingfield in long/lat degrees
    :param pos: LongLatCoordinate - coordinate to be converted
    :return: (delta_x, delta_y) - distances along axis
    """
    delta_x = 2 * EARTH_RADIUS * \
                 math.asin(
                     math.sqrt(math.cos(math.radians(bottom_left.lat)) * math.cos(math.radians(pos.lat)) *
                               math.sin(math.radians((pos.long - bottom_left.long) / 2)) ** 2))
    delta_y = 2 * EARTH_RADIUS * \
                math.asin(
                    math.sqrt(math.sin(math.radians((pos.lat - bottom_left.lat) / 2)) ** 2))
    if pos.long < bottom_left.long:
        delta_x *= -1
    if pos.lat < bottom_left.lat:
        delta_y *= -1
    return delta_x, delta_y


def lon_lat_to_grid(bottom_left_ll, resolution, coords):
    """
    Converts coordinates from longitude / latitude to our own "grid" coordinates. Resulting coordinates
    are floats that can be negative.
    :param bottom_left_ll: LongLatCoordinate - origin of the playingfield in long/lat degrees
    :param resolution: int - grid width in meters
    :param coords: LongLatCoordinate - coordinate to be converted
    :return: (long, lat) - converted coords
    """
    coords_m = haversin_lon_lat(bottom_left_ll, coords)
    x = coords_m[0] / resolution
    z = coords_m[1] / resolution
    return [x, z]


def point_to_coordinate2D(point: "LongLatCoordinate | APIWeightedCoordinate", area: "Area"):
    """
    Converts coordinates from longitude / latitude to our own "grid" Coordinate2D. Resulting coordinates
    are integer that can be negative.
    :param point: LongLatCoordinate | APIWeightedCoordinate - coordinate to be converted
    :param area: Area - contains resolution and bounds
    :return: Coordinate2D - converted point
    """
    x, y = lon_lat_to_grid(area.bottom_left, area.resolution, point)
    return Coordinate2D(math.floor(x), math.floor(y))
