import time
import math
import random

from Simulator import Coordinate4D

from .API import APISimulationConfig
from .Area import Area
from .Generator.Generator import Generator
from .Generator.MapTile import MapTile

from .config import available_allocators


def run_from_config(config: APISimulationConfig):
    if config.map.subselection is not None and config.map.subselection.bottomLeft and config.map.subselection.topRight:
        area = Area(config.map.subselection.bottomLeft, config.map.subselection.topRight, config.map.resolution)
    else:
        area = Area(config.map.bottomLeftCoordinate, config.map.topRightCoordinate, config.map.resolution)

    size = area.dimension

    dimensions = Coordinate4D(math.floor(size[0]),
                              math.floor(config.map.height / area.resolution),
                              math.floor(size[1]),
                              config.map.timesteps)

    maptiles = [MapTile(tile, area) for tile in config.map.tiles]

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
