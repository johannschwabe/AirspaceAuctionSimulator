import json
import random

from API import APISimulationConfig, build_json, run_from_config

random.seed(0)

f = open("new-zealand-simulation.json", "r")
converted = json.load(f)
config: APISimulationConfig = APISimulationConfig(**converted["config"])
f.close()

generator, duration = run_from_config(config)
print("--Simulation Completed--")
res = build_json(config.dict(), generator.simulator, duration)

f = open("test_sim.json", "w")
f.write(json.dumps(res))
f.close()
