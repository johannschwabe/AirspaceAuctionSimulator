import json
import math
import random
import time

from API import APISimulationConfig, Area, build_json
from API.Generator.Generator import Generator
from API.Generator.MapTile import MapTile
from API.config import available_allocators
from Simulator.Coordinates.Coordinate4D import Coordinate4D

random.seed(0)

f = open("config.json", "r")
config: APISimulationConfig = APISimulationConfig(**json.load(f))
f.close()

if config.map.subselection.bottomLeft and config.map.subselection.topRight:
    area = Area(config.map.subselection.bottomLeft, config.map.subselection.topRight, config.map.resolution)
else:
    area = Area(config.map.bottomLeftCoordinate, config.map.topRightCoordinate, config.map.resolution)

size = area.dimension

dimensions = Coordinate4D(math.floor(size[0]),
                          math.floor(config.map.height / area.resolution),
                          math.floor(size[1]),
                          config.map.timesteps)

maptiles = [MapTile(tile, area) for tile in config.map.tiles]

allocators = list(filter(lambda x: (x.__name__ == config.allocator), available_allocators))
allocator = allocators[0]()

payment_rule = [pf for pf in allocator.compatible_payment_functions() if
                pf.__name__ == config.paymentRule]
if len(payment_rule) != 1:
    raise Exception(f"{len(payment_rule)} payment functions found")
selected_payment_rule = payment_rule[0]()

g = Generator(config.owners, dimensions, maptiles, allocator, area, selected_payment_rule)
simulation_start_time = time.time_ns()
g.simulate()
simulation_end_time = time.time_ns()
simulation_duration = simulation_end_time - simulation_start_time
print("--Simulation Completed--")
res = build_json(config, g.simulator, simulation_duration)

f = open("test_sim.json", "w")
f.write(json.dumps(res))
f.close()
