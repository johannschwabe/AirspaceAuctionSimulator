"""
Run server using >>> uvicorn API:app --reload
App runs on 'https://localhost:8000/'
"""
import random
import time
from fastapi import HTTPException, FastAPI
from typing import List

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from Simulator.Coordinate import Coordinate4D
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


class APIGridCoordinates(BaseModel):
    x: int
    y: int
    lat: float
    long: float
    value: float


class APILocations(BaseModel):
    type: str
    gridCoordinates: List[APIGridCoordinates]


class APIOwner(BaseModel):
    color: str
    name: str
    agents: int
    minLocations: int
    maxLocations: int
    type: str
    allocator: str
    locations: List[APILocations]


class APIDimension(BaseModel):
    x: int
    y: int
    z: int
    t: int


class APISimpleCoordinates(BaseModel):
    long: float
    lat: float


class APIMap(BaseModel):
    coordinates: APISimpleCoordinates
    locationName: str
    neighbouringTiles: int
    topLeftCoordinate: APISimpleCoordinates
    bottomRightCoordinate: APISimpleCoordinates
    tiles: List[List[int]]


class APIAvailableOwner(BaseModel):
    label: str
    name: str
    description: str
    type: str
    allocator: str
    minLocations: int
    maxLocations: int


class APISimulationConfig(BaseModel):
    name: str
    description: str
    allocator: str
    dimension: APIDimension
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
             "_label": owner.label,
             "description": owner.description,
             "ownertype": "PathOwner" if issubclass(owner, PathOwner) else "SpaceOwner",
             "positions": owner.positions
             } for owner in allocator.compatible_owner()]


@app.post("/simulation")
def read_root(config: APISimulationConfig):
    dimensions = Coordinate4D(config.dimension.x, config.dimension.y, config.dimension.z, config.dimension.t)
    if config.map:
        top_left_coordinate = config.map.topLeftCoordinate
        bottom_right_coordinate = config.map.bottomRightCoordinate
        maptiles = [MapTile(tile, dimensions, top_left_coordinate, bottom_right_coordinate) for tile in
                    config.map.tiles]
    else:
        maptiles = []

    Coordinate4D.dim = dimensions

    allocators = list(filter(lambda x: (x.__name__ == config.allocator), available_allocators))
    if len(allocators) != 1:
        raise HTTPException(status_code=404, detail="allocator not found")
    allocator = allocators[0]()

    random.seed(2)
    g = Generator(owners=config.owners, dimensions=dimensions,
                  maptiles=maptiles, allocator=allocator)
    start_time = time.time_ns()
    g.simulate()
    end_time = time.time_ns()
    duration = int((end_time - start_time) / 1e9)
    print("--Simulation Completed--")
    json = build_json(config, g.simulator, duration)
    return json
