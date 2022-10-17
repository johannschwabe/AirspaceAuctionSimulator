import asyncio
import json
import random

from API import APISimulationConfig, run_from_config, generate_output

random.seed(4)

f = open("short-charlotta-simulation.json", "r")
converted = json.load(f)
config: APISimulationConfig = APISimulationConfig(**converted["config"])
# config: APISimulationConfig = APISimulationConfig(**converted)
f.close()

generator, duration = asyncio.run(run_from_config(config))
print("--Simulation Completed--")
simulation_output = generate_output(generator.simulator, duration, config.dict())

f = open("test_sim.json", "w")
f.write(json.dumps(simulation_output))
f.close()
