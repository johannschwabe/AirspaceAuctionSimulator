"""
Run server using >>> uvicorn API:app --reload
App runs on 'https://localhost:8000/'
"""
import random
import traceback

from fastapi import HTTPException, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Simulator import build_json
from .Runners import run_from_config
from .Types import APISimulationConfig
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
             "meta": bidding_strategy.meta()
             } for bidding_strategy in compatible_bidding_strategies]


@app.post("/simulation")
def simulate(config: APISimulationConfig):
    try:
        generator, duration = run_from_config(config)
    except ValueError as e:
        traceback.print_exc()
        raise HTTPException(status_code=404, detail=str(e))
    print("--Simulation Completed--")
    json = build_json(generator.simulator, duration)
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
