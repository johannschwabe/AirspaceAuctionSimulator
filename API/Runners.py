import time
import math
import random
from typing import Tuple, List

import mpmath as mp

from Simulator import Coordinate4D

from .API import APISimulationConfig
from .Area import Area
from .Types import APIWorldCoordinates
from .Generator.Generator import Generator
from .Generator.MapTile import MapTile

from .config import available_allocators


def tile2lon(z, x, y):
    return x / 2 ** z * 360 - 180


def tile2lat(z, x, y):
    n = mp.pi - 2 * mp.pi * y / 2 ** z
    return float((180 / mp.pi) * (mp.atan(0.5 * (mp.exp(n) - mp.exp(-n)))))


def tile_bbox(z, x, y) -> Tuple[APIWorldCoordinates, APIWorldCoordinates]:
    bottom_left_lat = tile2lat(z, x, y)
    bottom_left_lon = tile2lon(z, x, y)

    top_right_lat = tile2lat(z, x + 1, y + 1)
    top_right_lon = tile2lon(z, x + 1, y + 1)

    bottom_left = APIWorldCoordinates(lat=bottom_left_lat, long=bottom_left_lon)
    top_right = APIWorldCoordinates(lat=top_right_lat, long=top_right_lon)

    return bottom_left, top_right


def resolve_border_coordinates(tiles: List[List[int]]) -> Tuple[APIWorldCoordinates, APIWorldCoordinates]:
    n = len(tiles)
    top_right_tile_index = int(math.sqrt(n) - 1)
    top_right_tile = tiles[top_right_tile_index]

    bottom_left_tile_index = int(n - math.sqrt(n))
    bottom_left_tile = tiles[bottom_left_tile_index]

    top_righ_bb = tile_bbox(*top_right_tile)
    bottom_left_bb = tile_bbox(*bottom_left_tile)

    return bottom_left_bb[0], top_righ_bb[1]


def resolve_tiles(coordinates: APIWorldCoordinates, neighbouring_tiles: int) -> List[List[int]]:
    lat_rad = mp.radians(coordinates.lat)
    n = 2 ** 15

    xtile = int(n * ((coordinates.long + 180) / 360))
    ytile = int(n * (1 - (mp.log(mp.tan(lat_rad) + mp.sec(lat_rad)) / mp.pi)) / 2)

    tiles = []
    for i in range(-neighbouring_tiles, neighbouring_tiles + 1):
        for j in range(-neighbouring_tiles, neighbouring_tiles + 1):
            tiles.append([15, xtile + i, ytile + j])
    return tiles


def run_from_config(config: APISimulationConfig):
    tiles = resolve_tiles(config.map.coordinates, config.map.neighbouringTiles)
    if config.map.subselection is not None and config.map.subselection.bottomLeft and config.map.subselection.topRight:
        area = Area(config.map.subselection.bottomLeft, config.map.subselection.topRight, config.map.resolution)
    else:
        bottom_left_coordinate, top_right_coordinate = resolve_border_coordinates(tiles)
        area = Area(bottom_left_coordinate, top_right_coordinate, config.map.resolution)

    size = area.dimension

    dimensions = Coordinate4D(math.floor(size[0]),
                              math.floor(config.map.height / area.resolution),
                              math.floor(size[1]),
                              config.map.timesteps)

    maptiles = [MapTile(tile, area) for tile in tiles]

    allocators = list(filter(lambda x: (x.__name__ == config.allocator), available_allocators))
    if len(allocators) != 1:
        raise ValueError(f"Allocator {config.allocator} not found. Available are: {', '.join(available_allocators)}")
    allocator = allocators[0]()

    payment_rule = [pf for pf in allocator.compatible_payment_functions() if
                    pf.__name__ == config.paymentRule]
    if len(payment_rule) != 1:
        raise Exception(f"{len(payment_rule)} payment functions found")
    selected_payment_rule = payment_rule[0]()

    random.seed(2)
    generator = Generator(config.owners, dimensions, maptiles, allocator, area, selected_payment_rule)
    start_time = time.time_ns()
    generator.simulate()
    end_time = time.time_ns()
    duration = int((end_time - start_time) / 1e9)
    return generator, duration
