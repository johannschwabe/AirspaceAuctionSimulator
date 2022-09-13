import json
import random

from API import APISimulationConfig, build_json, run_from_config

random.seed(0)

f = open("Timor-Leste-config.json", "r")
config: APISimulationConfig = APISimulationConfig(**json.load(f))
f.close()

generator, duration = run_from_config(config)
print("--Simulation Completed--")
res = build_json(config.dict(), generator.simulator, duration)

f = open("test_sim.json", "w")
f.write(json.dumps(res))
f.close()
