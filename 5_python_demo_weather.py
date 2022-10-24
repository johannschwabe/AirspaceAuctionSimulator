import json
import random
from random import randint

from API import APIWorldCoordinates, Area, EnvironmentGen, GridLocation, LongLatCoordinate, MapTile, WebPathOwner, \
    generate_config, generate_output
from Demos.Priority import PriorityAllocator, PriorityPathBiddingStrategy, PriorityPathValueFunction, \
    PriorityPaymentRule
from Simulator import Coordinate3D, Coordinate4D, DynamicBlocker, Mechanism, Simulator, StaticBlocker

random.seed(3)

"""
Environment
"""

TIMESTEPS = 5000
ALLOCATION_PERIOD = 500

# Specifies a point in Zurich, Switzerland
coordinate = APIWorldCoordinates(long=8.542166566660185, lat=47.37175967132577)

# Resolves open-streetmap tiles around specified coordinate in Zurich
maptiles = MapTile.tiles_from_coordinates(coordinate)

# Bounding-Box spanned by zurich tile, which is needed to determine the size of our playing area
bottom_left_coordinate, top_right_coordinate = MapTile.bounding_box_from_maptiles_group(maptiles)

# Defines 2D area using both coordinates and given resolution (meters per voxel)
area = Area(bottom_left_coordinate, top_right_coordinate)

# Use area to find out play field resolution in voxels
[x, z] = area.dimension
y = 100  # Set map height to 100 voxels (which is also 100 meters since we have not specified a resolution)

# Define static blockers
st_peters_church = LongLatCoordinate(long=8.540776693388015, lat=47.3711851584472)
grossmuenster = LongLatCoordinate(long=8.544415750020427, lat=47.37011572741992)
fraumuenster = LongLatCoordinate(long=8.541375410621782, lat=47.36994730662017)
static_blockers = [
    StaticBlocker(location=area.point_to_coordinate3D(st_peters_church, 0), dimension=Coordinate3D(50, 50, 50)),
    StaticBlocker(location=area.point_to_coordinate3D(grossmuenster, 0), dimension=Coordinate3D(60, 60, 60)),
    StaticBlocker(location=area.point_to_coordinate3D(fraumuenster, 0), dimension=Coordinate3D(100, 100, 100)),
]

# Define dynamic (weather) blockers
dynamic_blockers = [
    DynamicBlocker([Coordinate4D(25 + (t // 2), 0, 400, t) for t in range(TIMESTEPS)],
                   dimension=Coordinate3D(50, 100, 300))
]

# Define environment
environment_generator = EnvironmentGen(
    dimensions=Coordinate4D(x, y, z, t=TIMESTEPS),
    maptiles=maptiles,
    map_area=area,
    blockers=[*static_blockers, *dynamic_blockers],
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
    color="#1e88e5",
    stops=[GridLocation("random"), GridLocation("random")],
    creation_ticks=[randint(0, ALLOCATION_PERIOD) for _ in range(100)],
    bidding_strategy=PriorityPathBiddingStrategy(),
    value_function=PriorityPathValueFunction(),
    near_radius=10,
    battery=10_000,
    speed=1,
    config={"priority": 0.15}
)

owners = [ownerA]

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
    name='Report Weather Demo Model',
    description='This model was generated using the 5_python_demo_weather.py Script',
    allocation_period=ALLOCATION_PERIOD,
)

# Generate simulation output that can be interpreted by the Visualizer
simulation_output = generate_output(simulator, simulation_time, simulation_config)

"""
Save to file
"""
with open('./Prefabs/configs/5_python_demo_weather-config.json', 'w') as f:
    f.write(json.dumps(simulation_config))

with open('./Prefabs/outputs/5_python_demo_weather-output.json', 'w') as f:
    f.write(json.dumps(simulation_output))
