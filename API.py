"""
Run server using >>> uvicorn API:app --reload
App runs on 'https://localhost:8000/'
"""
from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from Simulator.Coordinate import TimeCoordinate
from Simulator.Time import Tick
from Simulator.History import Generator

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
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

class SimulationConfigType(BaseModel):
    name: str
    description: Optional[str] = ""
    owners: List[OwnerType]
    dimension: DimensionType


@app.post("/simulation")
def read_root(config: SimulationConfigType):
    dimensions = TimeCoordinate(config.dimension.x, config.dimension.y, config.dimension.z, Tick(config.dimension.t))
    g = Generator(name=config.name, description=config.description, agents=100, owners=5, dimensions=dimensions, avg_flight_time=50)
    g.simulate()
    history = g.history
    return history.as_dict()

