import json
import random
from random import randint

from API import APIWorldCoordinates, Area, EnvironmentGen, GridLocation, LongLatCoordinate, MapTile, WebPathOwner, \
    generate_config, generate_output
from Demos.Priority import PriorityAllocator, PriorityPathBiddingStrategy, PriorityPathValueFunction, \
    PriorityPaymentRule
from Simulator import Coordinate4D, Mechanism, Simulator

random.seed(3)

"""
Environment
"""

TIMESTEPS = 1000
ALLOCATION_PERIOD = 250

# Specifies a point in Zurich, Switzerland
coordinate = APIWorldCoordinates(long=8.542166566660185, lat=47.37175967132577)

# Resolves open-streetmap tiles around specified coordinate in Zurich
maptiles = MapTile.tiles_from_coordinates(coordinate)

# Bounding-Box of our playing area inside the zurich tile
bottom_left_coordinate = APIWorldCoordinates(long=8.543278203323961, lat=47.36954866470366)
top_right_coordinate = APIWorldCoordinates(long=8.545048471709597, lat=47.370620437054555)

# Defines 2D area using both coordinates and given resolution (meters per voxel)
area = Area(bottom_left_coordinate, top_right_coordinate)

# Use area to find out play field resolution in voxels
[x, z] = area.dimension
y = 100  # Set map height to 100 voxels (which is also 100 meters since we have not specified a resolution)

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
    stops=[
        GridLocation("position",
                     area.point_to_coordinate2D(LongLatCoordinate(long=8.544116112079278, lat=47.37037820591456))),
        GridLocation("position",
                     area.point_to_coordinate2D(LongLatCoordinate(long=8.544689042330303, lat=47.36991197930435))),
    ],
    creation_ticks=[randint(0, ALLOCATION_PERIOD) for _ in range(50)],
    bidding_strategy=PriorityPathBiddingStrategy(),
    value_function=PriorityPathValueFunction(),
    near_radius=5,
    battery=5000,
    speed=1,
    config={"priority": 0.5}
)

ownerB = WebPathOwner(
    owner_id="1",
    name="OwnerB",
    color="#43a047",
    stops=[
        GridLocation("position",
                     area.point_to_coordinate2D(LongLatCoordinate(long=8.543771724602369, lat=47.36996647691119))),
        GridLocation("position",
                     area.point_to_coordinate2D(LongLatCoordinate(long=8.544431552514409, lat=47.37040971861829))),
    ],
    creation_ticks=[randint(0, ALLOCATION_PERIOD) for _ in range(50)],
    bidding_strategy=PriorityPathBiddingStrategy(),
    value_function=PriorityPathValueFunction(),
    near_radius=10,
    battery=5000,
    speed=1,
    config={"priority": 0.3}
)

ownerC = WebPathOwner(
    owner_id="2",
    name="OwnerC",
    color="#1e88e5",
    stops=[
        GridLocation("position",
                     area.point_to_coordinate2D(LongLatCoordinate(long=8.544399364191872, lat=47.37012270163643))),
        GridLocation("random"),
    ],
    creation_ticks=[randint(0, ALLOCATION_PERIOD) for _ in range(50)],
    bidding_strategy=PriorityPathBiddingStrategy(),
    value_function=PriorityPathValueFunction(),
    near_radius=2,
    battery=5000,
    speed=1,
    config={"priority": 1.0}
)

owners = [ownerA, ownerB, ownerC]

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
    name='Report Collision Model',
    description='This model was generated u sing the 3_python_demo_collisions.py Script',
    allocation_period=ALLOCATION_PERIOD,
)

# Generate simulation output that can be interpreted by the Visualizer
simulation_output = generate_output(simulator, simulation_time, simulation_config)

"""
Save to file
"""

with open('./Prefabs/configs/3_python_demo_collisions-config.json', 'w') as f:
    f.write(json.dumps(simulation_config))

with open('./Prefabs/outputs/3_python_demo_collisions-output.json', 'w') as f:
    f.write(json.dumps(simulation_output))
