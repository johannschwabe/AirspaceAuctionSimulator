import json
import random
from random import randint

from API import APIWorldCoordinates, Area, EnvironmentGen, GridLocation, MapTile, WebPathOwner, WebSpaceOwner, \
    generate_config, generate_output
from Demos.Priority import PriorityAllocator, PriorityPathBiddingStrategy, PriorityPathValueFunction, \
    PriorityPaymentRule, PrioritySpaceBiddingStrategy, PrioritySpaceValueFunction
from Simulator import Coordinate4D, Mechanism, Simulator

random.seed(3)

"""
Environment
"""

TIMESTEPS = 1000
ALLOCATION_PERIOD = 100

# Specifies a point in Lucerne, Switzerland
coordinate = APIWorldCoordinates(long=8.307432008121799, lat=47.05155777805148)

# Resolves open-streetmap tiles around specified coordinate in Zurich
maptiles = MapTile.tiles_from_coordinates(coordinate)

# Bounding-Box of our playing area inside the lucerne tile
bottom_left_coordinate = APIWorldCoordinates(long=8.306168879343144, lat=47.050397249055735)
top_right_coordinate = APIWorldCoordinates(long=8.309090737025008, lat=47.05278348678034)

# Defines 2D area using both coordinates and given resolution (meters per voxel)
area = Area(bottom_left_coordinate, top_right_coordinate)

# Use area to find out play field resolution in voxels
[x, z] = area.dimension
y = 50  # Set map height to 50 voxels (which is also 50 meters since we have not specified a resolution)

# Define environment
environment_generator = EnvironmentGen(
    dimensions=Coordinate4D(x, y, z, t=TIMESTEPS),
    maptiles=maptiles,
    map_area=area,
)

# Generate environment
environment = environment_generator.generate()

"""
Mechanism
"""

# Choose allocator, compatible payment rule and combine them into a mechanism
allocator = PriorityAllocator()
payment_rule = PriorityPaymentRule()
mechanism = Mechanism(allocator, payment_rule)

"""
Owners
"""
# Define owners that participate in simulation
ownerA = WebPathOwner(
    owner_id="0",
    name="OwnerA",
    color="#e53935",
    stops=[GridLocation("random"), GridLocation("random"), GridLocation("random")],
    creation_ticks=[randint(0, ALLOCATION_PERIOD) for _ in range(50)],
    bidding_strategy=PriorityPathBiddingStrategy(),
    value_function=PriorityPathValueFunction(),
    near_radius=5,
    battery=5000,
    speed=1,
    config={"priority": 0.5}
)

ownerB = WebSpaceOwner(
    owner_id="1",
    name="OwnerB",
    color="#1e88e5",
    stops=[GridLocation("random")],
    creation_ticks=[randint(0, ALLOCATION_PERIOD) for _ in range(100)],
    size=Coordinate4D(x=25, y=50, z=25, t=20),
    bidding_strategy=PrioritySpaceBiddingStrategy(),
    value_function=PrioritySpaceValueFunction(),
    config={"priority": 1.0}
)

owners = [ownerA, ownerB]

"""
Simulation
"""

# Create simulation
simulator = Simulator(owners, mechanism, environment)

# Run simulation for as long as ticks are left
simulation_time = simulator.run()

"""
Output
"""
# Generate config that can be interpreted by API
simulation_config = generate_config(
    simulator,
    environment_generator,
    name='Report Reallocation Model',
    description='This model was generated u sing the 2_python_demo_reallocations.py Script',
    allocation_period=ALLOCATION_PERIOD,
)

# Generate simulation output that can be interpreted by the Visualizer
simulation_output = generate_output(simulator, simulation_time, simulation_config)

"""
Save to file
"""
with open('./Prefabs/configs/2_python_demo_reallocations-config.json', 'w') as f:
    f.write(json.dumps(simulation_config))

with open('./Prefabs/outputs/2_python_demo_reallocations-output.json', 'w') as f:
    f.write(json.dumps(simulation_output))
