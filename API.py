"""
Run server using >>> uvicorn API:app --reload
App runs on 'https://localhost:8000/'
"""
import math
import random
from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from Simulator.Coordinate import TimeCoordinate
from Simulator.IO.JSONS import build_json
from Simulator.Time import Tick
from Simulator.Generator import Generator
from Simulator.Generator.MapTile import MapTile

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


class OwnerType(BaseModel):
    name: str
    color: str
    agents: int
    type: str


class DimensionType(BaseModel):
    x: int
    y: int
    z: int
    t: int


class SimpleCoordinateType(BaseModel):
    long: float
    lat: float


class MapType(BaseModel):
    tiles: List[List[int]]
    topLeftCoordinate: SimpleCoordinateType
    bottomRightCoordiante: SimpleCoordinateType


class SimulationConfigType(BaseModel):
    name: str
    description: Optional[str] = ""
    map: Optional[MapType] = None
    owners: List[OwnerType]
    dimension: DimensionType


@app.post("/simulation")
def read_root(config: SimulationConfigType):
    dimensions = TimeCoordinate(config.dimension.x, config.dimension.y, config.dimension.z, Tick(config.dimension.t))
    if config.map:
        topLeftCoordinate = config.map.topLeftCoordinate
        bottomRightCoordiante = config.map.bottomRightCoordiante
        maptiles = [MapTile(tile, dimensions, topLeftCoordinate, bottomRightCoordiante) for tile in config.map.tiles]
    else:
        maptiles = []

    TimeCoordinate.dim = dimensions

    random.seed(2)
    g = Generator(name=config.name, description=config.description, owners=config.owners, dimensions=dimensions,
                  maptiles=maptiles)
    g.simulate()
    print("--Simulation Completed--")
    json = build_json(g.simulator, g.name, g.description)
    return json
