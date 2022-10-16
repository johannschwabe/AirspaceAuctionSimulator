from random import randint
from time import time_ns
import json

from API import Area, APIWorldCoordinates, EnvironmentGen, MapTile, APISubselection, LongLatCoordinate, WebPathOwner, \
    WebSpaceOwner, GridLocation, generate_config, generate_output
from Demos.Priority import PriorityAllocator, PriorityPaymentRule, PriorityPathBiddingStrategy, \
    PriorityPathValueFunction, PrioritySpaceBiddingStrategy, PrioritySpaceValueFunction
from Simulator import Simulator, Coordinate4D, Mechanism

TIMESTEPS = 1000
ALLOCATION_PERIOD = 100

# Specifies a point in Zurich, Switzerland
coordinate = APIWorldCoordinates(lat=47.37175967132577, long=8.542166566660185)

# Resolves open-streetmap tiles around specified coordinate in Zurich
maptiles = MapTile.tiles_from_coordinates(coordinate)

# Bounding-Box spanned by zurich tile, which is needed to determine the size of our playing area
bottom_left_coordinate, top_right_coordinate = MapTile.bounding_box_from_maptiles_group(maptiles)

# Defines 2D area using both coordinates and given resolution (meters per voxel)
area = Area(bottom_left_coordinate, top_right_coordinate)

# Use area to find out play field resolution in voxels
[x, z] = area.dimension
y = 50 # Set map height to 50 voxels (which is also 50 meters since we have not specified a resolution)

# Define environment
environment_generator = EnvironmentGen(
    dimensions=Coordinate4D(x, y, z, t=TIMESTEPS),
    maptiles=maptiles,
    map_area=area,
    min_height=10
)

# Choose allocator, compatible payment rule and compatible mechanism
allocator = PriorityAllocator()
payment_rule = PriorityPaymentRule()
mechanism = Mechanism(allocator, payment_rule)

# Define owners that participate in simulation
owners = [
    WebPathOwner(
        owner_id="0",
        name="OwnerA",
        color="#ff0000",
        stops=[
            GridLocation("position", area.point_to_coordinate2D(LongLatCoordinate(47.371352787296225, 8.540492789574389))),
            GridLocation("position", area.point_to_coordinate2D(LongLatCoordinate(47.36562674969373, 8.546199997526907))),
        ],
        creation_ticks=[randint(0, ALLOCATION_PERIOD) for _ in range(50)],
        bidding_strategy=PriorityPathBiddingStrategy(),
        value_function=PriorityPathValueFunction(),
        near_radius=1,
        battery=2000,
        speed=1,
        config={"priority": 1.0}
    ),
    WebSpaceOwner(
        owner_id="2",
        name="OwnerB",
        color="#00ff00",
        stops=[GridLocation("random")],
        creation_ticks=[0, 0, 0, 10, 10, 10],
        size=Coordinate4D(x=20, y=5, z=20, t=50),
        bidding_strategy=PrioritySpaceBiddingStrategy(),
        value_function=PrioritySpaceValueFunction(),
        config={"priority": 0.5}
    ),
]

# Generate environment
environment = environment_generator.generate()

# Create simulation
simulator = Simulator(owners, mechanism, environment)

# Run simulation for as long as ticks are left
start = time_ns()
while simulator.tick():
    pass
simulation_time = time_ns() - start

# Generate config that can be interpreted by API
simulation_config = generate_config(
    simulator,
    environment_generator,
    name='Demo Model',
    description='This model was generated u sing the Demo.py Script',
    allocation_period=ALLOCATION_PERIOD,
)

# Generate simulation output that can be interpreted by API
simulation_output = generate_output(simulator, simulation_time, simulation_config)

with open('/Prefabs/configs/demo-config.json', 'w') as f:
    f.write(json.dumps(simulation_config))

with open('/Prefabs/outputs/demo-output.json', 'w') as f:
    f.write(json.dumps(simulation_output))
