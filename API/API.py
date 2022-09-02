"""
Run server using >>> uvicorn API:app --reload
App runs on 'https://localhost:8000/'
"""
import random

from fastapi import HTTPException, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Simulator import build_json

from .Types import APISimulationConfig
from .config import available_allocators
from .Runners import run_from_config

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
    try:
        generator, duration = run_from_config(config)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print("--Simulation Completed--")
    json = build_json(generator.simulator, duration)
    json["config"] = config
    return json
