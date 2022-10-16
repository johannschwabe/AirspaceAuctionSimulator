from random import randint
from time import time_ns
import json

from API import Area, APIWorldCoordinates, EnvironmentGen, MapTile, LongLatCoordinate, WebPathOwner, \
    WebSpaceOwner, GridLocation, generate_config, generate_output
from API.GridLocation.Heatmap import SparseHeatmap
from Demos.Priority import PriorityAllocator, PriorityPaymentRule, PriorityPathBiddingStrategy, \
    PriorityPathValueFunction, PrioritySpaceBiddingStrategy, PrioritySpaceValueFunction
from Simulator import Simulator, Coordinate4D, Mechanism

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
y = 100  # Set map height to 100 voxels (which is also 50 meters since we have not specified a resolution)

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
st_peters_church = LongLatCoordinate(long=8.540776693388015, lat=47.3711851584472)
grossmuenster = LongLatCoordinate(long=8.544415750020427, lat=47.37011572741992)

ownerA = WebPathOwner(
    owner_id="0",
    name="OwnerA",
    color="#ff0000",
    stops=[
        GridLocation("position", area.point_to_coordinate2D(st_peters_church)),
        GridLocation("position", area.point_to_coordinate2D(grossmuenster)),
    ],
    creation_ticks=[randint(0, ALLOCATION_PERIOD) for _ in range(10)],
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
    color="#00ff00",
    stops=[GridLocation("heatmap", heatmap=SparseHeatmap({
        area.point_to_coordinate2D(LongLatCoordinate(long=8.541896390368043, lat=47.37095173640276)): 0.2,
        area.point_to_coordinate2D(LongLatCoordinate(long=8.542409211750316, lat=47.3708928980311)): 0.5,
        area.point_to_coordinate2D(LongLatCoordinate(long=8.54322717892565, lat=47.37077808638756)): 0.3,
        area.point_to_coordinate2D(LongLatCoordinate(long=8.543979452409959, lat=47.370506842471464)): 0.3,
        area.point_to_coordinate2D(LongLatCoordinate(long=8.543771783498224, lat=47.37002462827945)): 0.2,
    }))],
    creation_ticks=[0, 0, 0, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800, 800, 900, 900],
    size=Coordinate4D(x=15, y=50, z=15, t=100),
    bidding_strategy=PrioritySpaceBiddingStrategy(),
    value_function=PrioritySpaceValueFunction(),
    config={"priority": 1.0}
)

fraumuenster = LongLatCoordinate(long=8.541375410621782, lat=47.36994730662017)

ownerC = WebPathOwner(
    owner_id="2",
    name="OwnerC",
    color="#0000ff",
    stops=[
        GridLocation("position", area.point_to_coordinate2D(fraumuenster)),
        GridLocation("random"),
    ],
    creation_ticks=[randint(0, ALLOCATION_PERIOD) for _ in range(50)],
    bidding_strategy=PriorityPathBiddingStrategy(),
    value_function=PriorityPathValueFunction(),
    near_radius=10,
    battery=10_000,
    speed=1,
    config={"priority": 0.15}
)

owners = [ownerA, ownerB, ownerC]

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
    name='Report Demo Model',
    description='This model was generated u sing the Demo.py Script',
    allocation_period=ALLOCATION_PERIOD,
)

# Generate simulation output that can be interpreted by API
simulation_output = generate_output(simulator, simulation_time, simulation_config)

with open('./Prefabs/configs/report-report-demo-config.json', 'w') as f:
    f.write(json.dumps(simulation_config))

with open('./Prefabs/outputs/report-report-demo-output.json', 'w') as f:
    f.write(json.dumps(simulation_output))
