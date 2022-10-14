from typing import List, TYPE_CHECKING

from API.WebClasses.BiddingStrategies.WebPathBiddingStrategy import WebPathBiddingStrategy
from API.WebClasses.Owners import WebOwnerMixin
from API.WebClasses.Owners.WebPathOwner import WebPathOwner
from API.WebClasses.Owners.WebSpaceOwner import WebSpaceOwner
from Simulator import GridLocationType
from . import Area
from .LongLatCoordinate import LongLatCoordinate
from .Types import APIBiddingStrategy, APILocations, APIMap, APIOwner, APISimulationConfig, APIWorldCoordinates

if TYPE_CHECKING:
    from .Generator.MapTile import MapTile
    from .Types import APISubselection
    from Simulator import Simulator


def generate_config(simulator: "Simulator",
                    subselection: "APISubselection",
                    map_tiles: List["MapTile"],
                    name: str = "Unknown"):
    bottom_left = LongLatCoordinate(subselection.bottomLeft.long, subselection.bottomLeft.lat)
    top_right = LongLatCoordinate(subselection.topRight.long, subselection.topRight.lat)
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
        allocationPeriod=simulator.environment.allocation_period,
        timesteps=dim.t,
        tiles=map_tile_ids
    )
    _owners = []
    for owner in simulator.owners:
        bs = owner.bidding_strategy
        meta = []
        assert isinstance(bs, WebPathBiddingStrategy)
        bs_meta = bs.meta()
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
        bidding_strategy = APIBiddingStrategy(label=bs.label,
                                              classname=bs.__class__.__name__,
                                              description=bs.description,
                                              allocationType=bs.allocation_type,
                                              minLocations=bs.min_locations,
                                              maxLocations=bs.max_locations,
                                              meta=meta)
        locations = []
        for stop in owner.stops:
            if stop.stop_type == GridLocationType.RANDOM.value:
                locations.append(APILocations(type=stop.stop_type, points=[]))
            elif stop.stop_type == GridLocationType.POSITION.value:
                posi = Area.LCS_to_long_lat(bottom_left, stop.position, resolution)
                locations.append(APILocations(type=stop.stop_type, points=[posi]))
        new_owner = APIOwner(
            color=owner.color if isinstance(owner, WebOwnerMixin) else hex(hash(owner.id) % 0xFFFFFF)[2:].zfill(6),
            name=owner.id,
            agents=len(owner.agents),
            biddingStrategy=bidding_strategy,
            locations=locations,
            valueFunction=owner.value_function.__class__.__name__)
        _owners.append(new_owner)
    return APISimulationConfig(name=name,
                               description="",
                               allocator=simulator.mechanism.allocator.__class__.__name__,
                               paymentRule=simulator.mechanism.payment_rule.__class__.__name__,
                               map=_map,
                               owners=_owners).dict()
