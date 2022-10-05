from API import Area
from API.LongLatCoordinate import LongLatCoordinate
from API.Types import APIMap, APISubselection, APISimulationConfig, APIWorldCoordinates, APIOwner, APIBiddingStrategy
from Simulator import Simulator


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
                                              clasname=bs.__name__,
                                              description=bs.description,
                                              allocationType=bs.allocation_type,
                                              minLocation=bs.min_locations,
                                              maxLocations=bs.max_locations,
                                              meta=bs.meta())
        new_owner = APIOwner(color=owner.color,
                             name=owner.name,
                             agents=len(owner.agents),
                             biddingStrategy=bidding_strategy,
                             locations=owner.stops,
                             valueFunction=owner.value_function.__name__)
        _owners.append(new_owner)
    _simi = APISimulationConfig(name=name,
                                description="",
                                allocator=simulator.mechanism.allocator.__name__,
                                paymentRule=simulator.mechanism.payment_rule.__name__,
                                map=_map,
                                owners=_owners)
