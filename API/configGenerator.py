from pydantic.fields import Field

from API import Area
from API.LongLatCoordinate import LongLatCoordinate
from API.Types import APIMap, APISubselection, APISimulationConfig, APIWorldCoordinates, APIOwner, APIBiddingStrategy, \
    APILocations
from Simulator import Simulator
from Simulator.Location.GridLocationType import GridLocationType


def generate_config(simulator: "Simulator", subselection: "APISubselection", name: "str" = "Unknown"):
    bottom_left = LongLatCoordinate(subselection.bottomLeft.long, subselection.bottomLeft.lat)
    top_right = LongLatCoordinate(subselection.topRight.long, subselection.topRight.lat)
    dim = simulator.environment.dimension
    dim_m = Area.haversin_lon_lat(bottom_left, top_right)
    resolution = round(dim_m[0] / dim.x)  # rounding needed?
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
        tiles=[]  # needed?
    )
    _owners = []
    for owner in simulator.owners:
        bs = owner.bidding_strategy
        bidding_strategy = APIBiddingStrategy(label=bs.label,
                                              classname=bs.__class__.__name__,
                                              description=bs.description,
                                              allocationType=bs.allocation_type,
                                              minLocations=bs.min_locations,
                                              maxLocations=bs.max_locations,
                                              meta=bs.meta())
        locations = []
        for stop in owner.stops:
            if stop.stop_type == GridLocationType.RANDOM.value:
                locations.append(APILocations(type=stop.stop_type))
            elif stop.stop_type == GridLocationType.POSITION.value:
                locations.append(APILocations(type=stop.stop_type, points=stop.position))
        new_owner = APIOwner(color=owner.color,
                             name=owner.name,
                             agents=len(owner.agents),
                             biddingStrategy=bidding_strategy,
                             locations=[APILocations(type=stop.stop_type,
                                                     points=[stop.position] if (
                                                         stop.stop_type == "position") else Field(None))
                                        for stop in owner.stops],
                             valueFunction=owner.value_function.__class__.__name__)
        _owners.append(new_owner)
    return APISimulationConfig(name=name,
                               description="",
                               allocator=simulator.mechanism.allocator.__class__.__name__,
                               paymentRule=simulator.mechanism.payment_rule.__class__.__name__,
                               map=_map,
                               owners=_owners)
