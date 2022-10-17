import asyncio
import json
import random

from API import APISimulationConfig, build_json, run_from_config

random.seed(4)

f = open("short-charlotta-simulation.json", "r")
converted = json.load(f)
config: APISimulationConfig = APISimulationConfig(**converted["config"])
# config: APISimulationConfig = APISimulationConfig(**converted)
f.close()

generator, duration = asyncio.run(run_from_config(config))
print("--Simulation Completed--")
res = build_json(config.dict(), generator, duration)

f = open("test_sim.json", "w")
f.write(json.dumps(res))
f.close()
