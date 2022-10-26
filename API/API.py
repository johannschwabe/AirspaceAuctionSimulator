"""
Run server using >>> uvicorn API:app --reload
App runs on 'https://localhost:8000/'
"""
import random
import time
import traceback
from typing import Any, Dict, TYPE_CHECKING

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from websockets import ConnectionClosedError

from Simulator import get_simulation_dict, get_statistics_dict
from .Runners import run_from_config
from .Types import APISimulationConfig
from .config import available_allocators

if TYPE_CHECKING:
    from .Generator.Generator import Generator

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


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, _websocket: WebSocket, client_id: str):
        await _websocket.accept()
        self.active_connections[client_id] = _websocket

    async def tick(self, client_id: str, percentage: float):
        if client_id not in self.active_connections:
            return False
        try:
            await self.active_connections[client_id].send_text(f"{percentage}")
        except ConnectionClosedError:
            return False
        return True

    def disconnect(self, client_id: str):
        del self.active_connections[client_id]


cm = ConnectionManager()


def build_json(config: Dict[str, Any], generator: "Generator", simulation_duration: int):
    simulation_json = get_simulation_dict(generator.simulator)
    statistics_start_time = time.time_ns()
    statistics = get_statistics_dict(generator.simulator)
    statistics_end_time = time.time_ns()
    statistics_duration = int((statistics_end_time - statistics_start_time) / 1e9)

    return {"config": config,
            "owner_map": {k: v.as_dict() for (k, v) in generator.owner_map.items()},
            "simulation": simulation_json,
            "statistics": statistics,
            "statistics_compute_time": statistics_duration,
            "simulation_compute_time": simulation_duration}


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


@app.post("/simulation/{client_id}")
async def simulate(config: "APISimulationConfig", client_id: str):
    try:
        generator, duration = await run_from_config(config, cm, client_id)
    except ValueError as e:
        traceback.print_exc()
        raise HTTPException(status_code=404, detail=str(e))
    print("--Simulation Completed--")
    if generator.simulator.time_step != generator.simulator.environment.dimension.t + 1:
        raise HTTPException(status_code=400, detail="Client aborted: Websocket disconnected")
    return build_json(config.dict(), generator, duration)


@app.get("/paymentRules/{allocator}")
def compatible_payment_rules(allocator):
    allocators = list(filter(lambda x: (x.__name__ == allocator), available_allocators))
    if len(allocators) != 1:
        return []
    selected_allocator = allocators[0]
    return [{"classname": payment_function.__name__, "label": payment_function.label} for payment_function in
            selected_allocator.compatible_payment_functions()]


@app.websocket("/api/ws/{client_id}")
async def websocket(_websocket: WebSocket, client_id: str):
    await cm.connect(_websocket, client_id)
    try:
        while True:
            data = await _websocket.receive_text()
            print(data)
    except WebSocketDisconnect:
        cm.disconnect(client_id=client_id)
        print(client_id + " disconnected")
