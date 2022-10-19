import time
from typing import List, Optional, TYPE_CHECKING, Tuple

from Simulator import Coordinate4D
from .Area import Area
from .Generator.Generator import Generator
from .Generator.MapTile import MapTile
from .Types import APIWorldCoordinates
from .config import available_allocators

if TYPE_CHECKING:
    from .API import ConnectionManager
    from .Types import APISimulationConfig


def init_generator(config: "APISimulationConfig",
                   connection_manager: Optional["ConnectionManager"] = None,
                   client_id: Optional[str] = None) -> "Generator":
    maptiles: List["MapTile"] = MapTile.tiles_from_coordinates(config.map.coordinates, config.map.neighbouringTiles,
                                                               config.map.resolution)
    config.map.tiles = [tile.zxy for tile in maptiles]

    if config.map.subselection is not None and config.map.subselection.bottomLeft and config.map.subselection.topRight:
        map_playing_field_area = Area(config.map.subselection.bottomLeft, config.map.subselection.topRight,
                                      config.map.resolution,
                                      config.map.minHeight)
    else:
        bottom_left_coordinate, top_right_coordinate = MapTile.bounding_box_from_maptiles_group(maptiles)
        config.map.bottomLeftCoordinate = bottom_left_coordinate.as_dict()
        config.map.topRightCoordinate = top_right_coordinate.as_dict()
        map_playing_field_area = Area(APIWorldCoordinates(lat=bottom_left_coordinate.lat,
                                                          long=bottom_left_coordinate.long),
                                      APIWorldCoordinates(lat=top_right_coordinate.lat,
                                                          long=top_right_coordinate.long),
                                      config.map.resolution,
                                      config.map.minHeight)

    size = map_playing_field_area.dimension

    dimensions = Coordinate4D(size[0],
                              config.map.height / map_playing_field_area.resolution,
                              size[1],
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

    generator = Generator(config.owners, dimensions, maptiles, allocator, map_playing_field_area, selected_payment_rule,
                          allocation_period=config.map.allocationPeriod, connection_manager=connection_manager,
                          client_id=client_id)
    return generator


async def run_from_config(config: "APISimulationConfig",
                          connection_manager: Optional["ConnectionManager"] = None,
                          client_id: Optional[str] = None) -> Tuple[Generator, int]:
    """
    Runs an AirspaceAuctionSimulation using a config that is provided by the API.
    :param client_id:
    :param connection_manager:
    :param config: Configuration object, defining all parameters of the Simulation
    :return: Simulated generator, simulation duration in seconds
    """
    generator = init_generator(config, connection_manager, client_id)
    start_time = time.time_ns()
    await generator.simulate()
    end_time = time.time_ns()
    duration = int((end_time - start_time) / 1e9)
    return generator, duration


def run_from_config_for_cli(config: "APISimulationConfig") -> Tuple[Generator, int]:
    """
    Runs an AirspaceAuctionSimulation using a config that is generated using the CLI.
    :param config: Configuration object, defining all parameters of the Simulation
    :return: Simulated generator, simulation duration in seconds
    """
    generator = init_generator(config)
    start_time = time.time_ns()
    generator.simulate_cli()
    end_time = time.time_ns()
    duration = int((end_time - start_time) / 1e9)
    return generator, duration
