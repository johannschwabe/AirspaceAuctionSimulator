"""
Run server using >>> uvicorn API:app --reload
App runs on 'https://localhost:8000/'
"""
import math
import random
import time
from fastapi import HTTPException, FastAPI
from typing import List, Optional

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic.fields import Field

from CoordinateTransformations import from_lon_lat, to_lon_lat
from Simulator.Coordinate import Coordinate4D
from Simulator.Generator.Area import Area
from Simulator.IO.JSONS import build_json
from Simulator.Generator import Generator
from Simulator.Generator.MapTile import MapTile
from Simulator.Owner import PathOwner
from config import available_allocators

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
class APISimpleCoordinates(BaseModel):
    long: float
    lat: float

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

class APIMap(BaseModel):
    coordinates: APISimpleCoordinates
    locationName: str
    neighbouringTiles: int
    bottomLeftCoordinate: APISimpleCoordinates
    topRightCoordinate: APISimpleCoordinates
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
    meta: list[object]


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
             "ownerType": "PathOwner" if issubclass(owner, PathOwner) else "SpaceOwner",
             "minLocations": owner.min_locations,
             "maxLocations": owner.max_locations
             } for owner in allocator.compatible_owner()]


@app.post("/simulation")
def read_root(config: APISimulationConfig):
    if config.map.subselection.bottomLeft and config.map.subselection.topRight:
        bottom_left_pm = from_lon_lat([config.map.subselection.bottomLeft.long, config.map.subselection.bottomLeft.lat])
        top_right_pm = from_lon_lat([config.map.subselection.topRight.long, config.map.subselection.topRight.lat])
    else:
        bottom_left_pm = from_lon_lat([config.map.bottomLeftCoordinate.long, config.map.bottomLeftCoordinate.lat])
        top_right_pm = from_lon_lat([config.map.topRightCoordinate.long, config.map.topRightCoordinate.lat])

    size = [top_right_pm[0] - bottom_left_pm[0], top_right_pm[1] - bottom_left_pm[1]]
    resolution = config.map.resolution

    dimensions = Coordinate4D(math.ceil(size[0]/resolution),
                              config.map.height,
                              math.ceil(size[1]/resolution),
                              config.map.timesteps)
    area = Area(config.map.subselection.bottomLeft, config.map.subselection.topRight, config.map.resolution) if config.map.subselection.topRight and config.map.subselection.bottomLeft else \
        Area(config.map.bottomLeftCoordinate, config.map.topRightCoordinate, config.map.resolution)
    maptiles = [MapTile(tile, dimensions, area) for tile in
                config.map.tiles]


    Coordinate4D.dim = dimensions

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
    json = build_json(config, g.simulator, duration)
    return json
