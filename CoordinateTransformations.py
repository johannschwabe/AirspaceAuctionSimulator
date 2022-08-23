import math
from typing import TYPE_CHECKING

EARTH_RADIUS = 6371008.8
from Simulator.Coordinate import Coordinate2D

if TYPE_CHECKING:
    from API import APIWeightedCoordinate
    from Simulator.Generator.Area import LongLatCoordinate, Area

def haversin_lon_lat(bottom_left, pos):
    delta_long = 2 * EARTH_RADIUS * \
           math.asin(
               math.sqrt(math.cos(math.radians(bottom_left.lat)) * math.cos(math.radians(pos.lat)) *
                         math.sin(math.radians((pos.long - bottom_left.long) / 2)) ** 2))
    delta_lat = 2 * EARTH_RADIUS * \
           math.asin(
               math.sqrt(math.sin(math.radians((pos.lat - bottom_left.lat)/2)) ** 2))
    if pos.long < bottom_left.long:
        delta_long *= -1
    if pos.lat < bottom_left.lat:
        delta_lat *= -1
    return delta_long, delta_lat

def lon_lat_to_grid(bottom_left_ll, resolution, coords):
    coords_m = haversin_lon_lat(bottom_left_ll, coords)
    x = coords_m[0] / resolution
    z = coords_m[1] / resolution
    return [x, z]


def point_to_coordinate2D(point: "LongLatCoordinate | APIWeightedCoordinate", area: "Area"):
    x, y = lon_lat_to_grid(area.bottom_left, area.resolution, point)
    return Coordinate2D(math.floor(x), math.floor(y))
