"""
Run server using >>> uvicorn API:app --reload
App runs on 'https://localhost:8000/'
"""
import math
import random
import time
from typing import List, Optional, Dict, Any

from fastapi import HTTPException, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic.fields import Field

from Simulator import Coordinate4D, build_json
from .Area import Area
from .Generator.Generator import Generator
from .Generator.MapTile import MapTile
from .config import available_allocators

app = FastAPI()

random.seed(2)

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5050",
    "*",  # REMOVE for production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class APIWorldCoordinates(BaseModel):
    long: float
    lat: float


class APIWeightedCoordinate(BaseModel):
    lat: float
    long: float
    value: float


class APISubselection(BaseModel):
    bottomLeft: Optional["APIWorldCoordinates"] = Field(None)
    topRight: Optional["APIWorldCoordinates"] = Field(None)


class APILocations(BaseModel):
    type: str
    points: List[APIWeightedCoordinate]


class APIBiddingStrategy(BaseModel):
    minLocations: int
    maxLocations: int
    allocationType: str
    classname: str
    meta: List[Dict[str, Any]]


class APIOwner(BaseModel):
    color: str
    name: str
    agents: int
    biddingStrategy: APIBiddingStrategy
    locations: List[APILocations]
    valueFunction: str


class APIMap(BaseModel):
    coordinates: APIWorldCoordinates
    locationName: str
    neighbouringTiles: int
    bottomLeftCoordinate: APIWorldCoordinates
    topRightCoordinate: APIWorldCoordinates
    subselection: APISubselection
    resolution: int
    tiles: List[List[int]]
    height: int
    timesteps: int


class APISimulationConfig(BaseModel):
    name: str
    description: str
    allocator: str
    map: APIMap
    owners: List[APIOwner]
    paymentRule: str


@app.get("/allocators")
def get_allocators():
    return [_allocator.__name__ for _allocator in available_allocators]


@app.get("/valueFunctions/{allocator}/{bidding_strategy}")
def get_value_functions(allocator, bidding_strategy):
    allocators = list(filter(lambda x: (x.__name__ == allocator), available_allocators))
    if len(allocators) != 1:
        return []
    selected_allocator = allocators[0]
    bidding_strategies = list(
        filter(lambda x: (x.__name__ == bidding_strategy), selected_allocator.compatible_bidding_strategies()))
    if len(bidding_strategies) != 1:
        return []
    selected_bidding_strategy = bidding_strategies[0]
    return [{"classname": value_function.__name__,
             "label": value_function.label,
             "description": value_function.description} for value_function in
            selected_bidding_strategy.compatible_value_functions()]


@app.get("/biddingStrategies/{allocator}")
def get_strategies_for_allocator(allocator):
    print(available_allocators[0])
    allocators = list(filter(lambda x: (x.__name__ == allocator), available_allocators))
    if len(allocators) != 1:
        return []
    selected_allocator = allocators[0]
    compatible_bidding_strategies = selected_allocator.compatible_bidding_strategies()
    return [{"classname": bidding_strategy.__name__,
             "label": bidding_strategy.label,
             "description": bidding_strategy.description,
             "strategyType": bidding_strategy.allocation_type,
             "minLocations": bidding_strategy.min_locations,
             "maxLocations": bidding_strategy.max_locations,
             "meta": bidding_strategy.meta
             } for bidding_strategy in compatible_bidding_strategies]


@app.post("/simulation")
def read_root(config: APISimulationConfig):
    if config.map.subselection.bottomLeft and config.map.subselection.topRight:
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
        raise HTTPException(status_code=404, detail="allocator not found")
    allocator = allocators[0]()

    payment_rule = [pf for pf in allocator.compatible_payment_functions() if
                    pf.__name__ == config.paymentRule]
    if len(payment_rule) != 1:
        raise Exception(f"{len(payment_rule)} payment functions found")
    selected_payment_rule = payment_rule[0]()

    random.seed(2)
    g = Generator(config.owners, dimensions, maptiles, allocator, area, selected_payment_rule)
    start_time = time.time_ns()
    g.simulate()
    end_time = time.time_ns()
    duration = int((end_time - start_time) / 1e9)
    print("--Simulation Completed--")
    json = build_json(g.simulator, duration)
    json["config"] = config
    return json


@app.get("/paymentRules/{allocator}")
def compatible_payment_rules(allocator):
    allocators = list(filter(lambda x: (x.__name__ == allocator), available_allocators))
    if len(allocators) != 1:
        return []
    selected_allocator = allocators[0]
    return [{"classname": payment_function.__name__, "label": payment_function.label} for payment_function in
            selected_allocator.compatible_payment_functions()]
