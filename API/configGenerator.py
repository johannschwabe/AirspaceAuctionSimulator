from typing import Optional, TYPE_CHECKING

from Simulator.Coordinates.Coordinate2D import Coordinate2D
from . import Area
from .GridLocation.GridLocationType import GridLocationType
from .GridLocation.HeatmapType import HeatmapType
from .Types import APIBiddingStrategy, APILocations, APIMap, APIOwner, APISimulationConfig, APISubselection, \
    APIWeightedCoordinate, APIWorldCoordinates
from .WebClasses.BiddingStrategies.WebBiddingStrategy import WebBiddingStrategy
from .WebClasses.Owners.WebPathOwner import WebPathOwner
from .WebClasses.Owners.WebSpaceOwner import WebSpaceOwner

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
        assert isinstance(bidding_strategy, WebBiddingStrategy)
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
                locations.append(APILocations(type=GridLocationType.RANDOM.value, points=[]))
            elif stop.grid_location_type == GridLocationType.POSITION.value:
                posi = Area.LCS_to_long_lat(bottom_left, stop.position, resolution)
                weighted_coordiante = APIWeightedCoordinate(lat=posi.lat, long=posi.long, value=1)
                locations.append(APILocations(type=stop.grid_location_type, points=[weighted_coordiante]))
            elif stop.grid_location_type == GridLocationType.HEATMAP.value:
                posis = []
                if stop.heatmap.heatmap_type == HeatmapType.SPARSE.value:
                    for posi, value in stop.heatmap.sparse.items():
                        conv_posi = Area.LCS_to_long_lat(bottom_left, posi, resolution)
                        posis.append(APIWeightedCoordinate(lat=conv_posi.lat, long=conv_posi.long, value=value))
                elif stop.heatmap.heatmap_type == HeatmapType.INVERSE_SPARSE.value:
                    for value, _posis in stop.heatmap.inverse_sparse.items():
                        for posi in _posis:
                            conv_posi = Area.LCS_to_long_lat(bottom_left, posi, resolution)
                            posis.append(
                                APIWeightedCoordinate(lat=conv_posi.lat, long=conv_posi.long, value=float(value)))
                elif stop.heatmap.heatmap_type == HeatmapType.MATRIX.value:
                    for x, row in enumerate(stop.heatmap.matrix):
                        for z, val in enumerate(row):
                            if val > 0:
                                conv_posi = Area.LCS_to_long_lat(bottom_left, Coordinate2D(x, z), resolution)
                                posis.append(
                                    APIWeightedCoordinate(lat=conv_posi.lat, long=conv_posi.long, value=val))
                locations.append(APILocations(type=GridLocationType.HEATMAP.value, points=posis))

        new_owner = APIOwner(
            color=owner.color if isinstance(owner, WebPathOwner) or isinstance(owner, WebSpaceOwner) else hex(
                hash(owner.id) % 0xFFFFFF)[2:].zfill(6),
            name=owner.name,
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
