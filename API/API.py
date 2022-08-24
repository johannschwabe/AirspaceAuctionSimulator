"""
Run server using >>> uvicorn API:app --reload
App runs on 'https://localhost:8000/'
"""
import math
import random
import time
from typing import List, Optional

from fastapi import HTTPException, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic.fields import Field

from Simulator import Coordinate4D, build_json
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

class APIWeightedCoordinate(BaseModel):
    lat: float
    long: float
    value: float

class APISubselection(BaseModel):
    bottomLeft: Optional[APISimpleCoordinates] = Field(None)
    topRight: Optional[APISimpleCoordinates] = Field(None)

class APILocations(BaseModel):
    type: str
    points: List[APIWeightedCoordinate]


class APIOwner(BaseModel):
    color: str
    name: str
    agents: int
    minLocations: int
    maxLocations: int
    type: str
    classname: str
    allocator: str
    locations: List[APILocations]


class APIWorldCoordinates(BaseModel):
    long: float
    lat: float


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


class APIAvailableOwner(BaseModel):
    label: str
    classname: str
    description: str
    ownerType: str
    allocator: str
    minLocations: int
    maxLocations: int
    meta: List[object]


class APISimulationConfig(BaseModel):
    name: str
    description: str
    allocator: str
    map: APIMap
    owners: List[APIOwner]
    availableAllocators: List[str]
    availableOwnersForAllocator: List[APIAvailableOwner]


@app.get("/allocators")
def get_allocators():
    return [_allocator.__name__ for _allocator in available_allocators]


@app.get("/owners/{allocator_name}")
def get_owners_for_allocator(allocator_name):
    allocators = list(filter(lambda x: (x.__name__ == allocator_name), available_allocators))
    if len(allocators) != 1:
        return []
    allocator = allocators[0]
    return [{"classname": owner.__name__,
             "label": owner.label,
             "meta": owner.meta,
             "description": owner.description,
             "ownerType": owner.allocation_type,
             "minLocations": owner.min_locations,
             "maxLocations": owner.max_locations
             } for owner in allocator.compatible_owner()]


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

    maptiles = [MapTile(tile, area) for tile in
                config.map.tiles]

    allocators = list(filter(lambda x: (x.__name__ == config.allocator), available_allocators))
    if len(allocators) != 1:
        raise HTTPException(status_code=404, detail="allocator not found")
    allocator = allocators[0]()

    random.seed(2)
    g = Generator(owners=config.owners, dimensions=dimensions,
                  maptiles=maptiles, allocator=allocator, area=area)
    start_time = time.time_ns()
    g.simulate()
    end_time = time.time_ns()
    duration = int((end_time - start_time) / 1e9)
    print("--Simulation Completed--")
    json = build_json(g.simulator, duration)
    json["config"] = config
    return json
