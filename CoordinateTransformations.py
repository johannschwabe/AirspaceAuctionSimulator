import math
from typing import TYPE_CHECKING

from pyproj import Transformer

from Simulator.Coordinate import Coordinate2D

if TYPE_CHECKING:
    from API import APIWeightedCoordinate
    from Simulator.Generator.Area import LongLatCoordinate, Area

from_lon_lat_transformer = Transformer.from_crs(4326, 3857, always_xy=True)
to_lon_lat_transformer = Transformer.from_crs(3857, 4326, always_xy=True)


def to_lon_lat(pm_coordinates):
    return to_lon_lat_transformer.transform(pm_coordinates[0], pm_coordinates[1])


def from_lon_lat(ll_coordinates):
    return from_lon_lat_transformer.transform(ll_coordinates[0], ll_coordinates[1], )


def lon_lat_to_grid(bottom_left_ll, resolution, coords):
    bottom_left_pm = from_lon_lat(bottom_left_ll)
    coords_pm = from_lon_lat(coords)
    x = (coords_pm[0] - bottom_left_pm[0]) / resolution
    z = (coords_pm[1] - bottom_left_pm[1]) / resolution
    return [x, z]


def point_to_coordinate2D(point: "LongLatCoordinate | APIWeightedCoordinate", area: "Area"):
    x, y = lon_lat_to_grid([area.bottom_left.long, area.bottom_left.lat], area.resolution, [point.long, point.lat])
    return Coordinate2D(math.floor(x), math.floor(y))
