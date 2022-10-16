from typing import Optional, TYPE_CHECKING

from API.WebClasses.BiddingStrategies.WebPathBiddingStrategy import WebPathBiddingStrategy
from API.WebClasses.Owners.WebPathOwner import WebPathOwner
from API.WebClasses.Owners.WebSpaceOwner import WebSpaceOwner
from . import Area
from .GridLocation.GridLocationType import GridLocationType
from .Types import APIBiddingStrategy, APILocations, APIMap, APIOwner, APISimulationConfig, APIWorldCoordinates
from .Types import APISubselection

if TYPE_CHECKING:
    from .Generator.EnvironmentGen import EnvironmentGen
    from Simulator import Simulator


def generate_config(simulator: "Simulator",
                    environment_generator: 'EnvironmentGen',
                    name: str = "Unknown Model",
                    description: str = "No Description provided",
                    allocation_period: Optional[int] = None):
    map_tiles = environment_generator.maptiles
    bottom_left = environment_generator.map_area.bottom_left
    top_right = environment_generator.map_area.top_right
    subselection = APISubselection(
        bottomLeft=APIWorldCoordinates(long=bottom_left.long, lat=bottom_left.lat),
        topRight=APIWorldCoordinates(long=top_right.long, lat=top_right.lat),
    )
    dim = simulator.environment.dimension
    dim_m = Area.haversin_lon_lat(bottom_left, top_right)
    resolution = round(dim_m[0] / dim.x)  # rounding needed?
    map_tile_ids = [(tile.z, tile.x, tile.y) for tile in map_tiles]
    _map = APIMap(
        coordinates=APIWorldCoordinates(
            long=(bottom_left.long + top_right.long) / 2,
            lat=(bottom_left.lat + top_right.lat) / 2),
        locationName="-",
        neighbouringTiles=0,
        bottomLeftCoordinate=subselection.bottomLeft,
        topRightCoordinate=subselection.topRight,
        subselection=subselection,
        resolution=resolution,
        height=dim.y * resolution,
        minHeight=simulator.environment.min_height * resolution,
        allocationPeriod=allocation_period if allocation_period is not None else simulator.environment.dimension.t,
        timesteps=dim.t,
        tiles=map_tile_ids
    )
    _owners = []
    for owner in simulator.owners:
        bidding_strategy = owner.bidding_strategy
        meta = []
        assert isinstance(bidding_strategy, WebPathBiddingStrategy)
        bs_meta = bidding_strategy.meta()
        if isinstance(owner, WebPathOwner):
            for meta_field in bs_meta:
                if meta_field["key"] == "near_field":
                    meta_field["value"] = owner.near_radius
                    meta.append(meta_field)
                    continue
                if meta_field["key"] == "battery":
                    meta_field["value"] = owner.battery
                    meta.append(meta_field)
                    continue
                if meta_field["key"] == "speed":
                    meta_field["value"] = owner.speed
                    meta.append(meta_field)
                    continue
                meta_field["value"] = owner.config[meta_field["key"]]
                meta.append(meta_field)
        elif isinstance(owner, WebSpaceOwner):
            for meta_field in bs_meta:
                if meta_field["key"] == "size_x":
                    meta_field["value"] = owner.size.x
                    meta.append(meta_field)
                    continue
                if meta_field["key"] == "size_y":
                    meta_field["value"] = owner.size.y
                    meta.append(meta_field)
                    continue
                if meta_field["key"] == "size_z":
                    meta_field["value"] = owner.size.z
                    meta.append(meta_field)
                    continue
                if meta_field["key"] == "size_t":
                    meta_field["value"] = owner.size.t
                    meta.append(meta_field)
                    continue
                meta_field["value"] = owner.config[meta_field["key"]]
                meta.append(meta_field)
        else:
            for meta_field in bs_meta:
                meta_field["value"] = owner.config[meta_field["key"]]
                meta.append(meta_field)
        bidding_strategy = APIBiddingStrategy(label=bidding_strategy.label,
                                              classname=bidding_strategy.__class__.__name__,
                                              description=bidding_strategy.description,
                                              allocationType=bidding_strategy.allocation_type,
                                              minLocations=bidding_strategy.min_locations,
                                              maxLocations=bidding_strategy.max_locations,
                                              meta=meta)
        locations = []
        for stop in owner.stops:
            if stop.grid_location_type == GridLocationType.RANDOM.value:
                locations.append(APILocations(type=stop.grid_location_type, points=[]))
            elif stop.grid_location_type == GridLocationType.POSITION.value:
                posi = Area.LCS_to_long_lat(bottom_left, stop.position, resolution)
                locations.append(APILocations(type=stop.grid_location_type, points=[posi]))
        new_owner = APIOwner(
            color=owner.color if isinstance(owner, WebPathOwner) or isinstance(owner, WebSpaceOwner) else hex(
                hash(owner.id) % 0xFFFFFF)[2:].zfill(6),
            name=owner.id,
            agents=len(owner.agents),
            biddingStrategy=bidding_strategy,
            locations=locations,
            valueFunction=owner.value_function.__class__.__name__)
        _owners.append(new_owner)
    return APISimulationConfig(name=name,
                               description=description,
                               allocator=simulator.mechanism.allocator.__class__.__name__,
                               paymentRule=simulator.mechanism.payment_rule.__class__.__name__,
                               map=_map,
                               owners=_owners).dict()
