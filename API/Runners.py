import time
import math
import random
from typing import List, Tuple

from Simulator import Coordinate4D

from .API import APISimulationConfig
from .Area import Area
from .Generator.Generator import Generator
from .Generator.MapTile import MapTile

from .config import available_allocators

def run_from_config(config: APISimulationConfig) -> Tuple[Generator, int]:
    """
    Runs an AirspaceAuctionSimulation using a config that is usually provided by the API or generated using the CLI.
    :param config: Configuration object, defining all parameters of the Simulation
    :return: Simulated generator, simulation duration in seconds
    """
    maptiles: List[MapTile] = MapTile.tiles_from_coordinates(config.map.coordinates, config.map.neighbouringTiles, config.map.resolution)
    config.map.tiles = [tile.zxy for tile in maptiles]

    if config.map.subselection is not None and config.map.subselection.bottomLeft and config.map.subselection.topRight:
        area = Area(config.map.subselection.bottomLeft, config.map.subselection.topRight, config.map.resolution)
    else:
        bottom_left_coordinate, top_right_coordinate = MapTile.bounding_box_from_maptiles_group(maptiles)
        config.map.bottomLeftCoordinate = bottom_left_coordinate
        config.map.topRightCoordinate = top_right_coordinate
        area = Area(bottom_left_coordinate, top_right_coordinate, config.map.resolution)

    print(area)
    size = area.dimension

    dimensions = Coordinate4D(math.floor(size[0]),
                              math.floor(config.map.height / area.resolution),
                              math.floor(size[1]),
                              config.map.timesteps)

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
