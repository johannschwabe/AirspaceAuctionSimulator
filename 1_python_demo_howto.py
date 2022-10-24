import json
import random
from random import randint

from API import APIWorldCoordinates, Area, EnvironmentGen, GridLocation, LongLatCoordinate, MapTile, SparseHeatmap, \
    WebPathOwner, WebSpaceOwner, generate_config, generate_output
from Demos.Priority import PriorityAllocator, PriorityPathBiddingStrategy, PriorityPathValueFunction, \
    PriorityPaymentRule, PrioritySpaceBiddingStrategy, PrioritySpaceValueFunction
from Simulator import Coordinate4D, Mechanism, Simulator

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

# Create stops for the path owner
st_peters_church = LongLatCoordinate(long=8.540776693388015, lat=47.3711851584472)
grossmuenster = LongLatCoordinate(long=8.544415750020427, lat=47.37011572741992)

# Translate real world coordinates to grid-locations
st_peters_church_stop = GridLocation("position", area.point_to_coordinate2D(st_peters_church))
grossmuenster_stop = GridLocation("position", area.point_to_coordinate2D(grossmuenster))

# Create a path owner flying from the St. Peters Church to the Grossmünster
ownerA = WebPathOwner(
    owner_id="0",
    name="OwnerA",
    color="#e53935",
    stops=[st_peters_church_stop, grossmuenster_stop],
    creation_ticks=[randint(0, ALLOCATION_PERIOD) for _ in range(10)],
    bidding_strategy=PriorityPathBiddingStrategy(),
    value_function=PriorityPathValueFunction(),
    near_radius=5,
    battery=5000,
    speed=1,
    config={"priority": 0.5}
)

# Create a sparse heatmap that defines the locations for the space owners agents
heatmap = SparseHeatmap({
    area.point_to_coordinate2D(LongLatCoordinate(long=8.541896390368043, lat=47.37095173640276)): 0.2,
    area.point_to_coordinate2D(LongLatCoordinate(long=8.542409211750316, lat=47.3708928980311)): 0.5,
    area.point_to_coordinate2D(LongLatCoordinate(long=8.54322717892565, lat=47.37077808638756)): 0.3,
    area.point_to_coordinate2D(LongLatCoordinate(long=8.543979452409959, lat=47.370506842471464)): 0.3,
    area.point_to_coordinate2D(LongLatCoordinate(long=8.543771783498224, lat=47.37002462827945)): 0.2,
})
heatmap_stop = GridLocation("heatmap", heatmap=heatmap)

# Create a space owner with agents each requesting one of the positions in the heatmap
ownerB = WebSpaceOwner(
    owner_id="1",
    name="OwnerB",
    color="#43a047",
    stops=[heatmap_stop],
    creation_ticks=[0, 0, 0, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800, 800, 900, 900],
    size=Coordinate4D(x=15, y=50, z=15, t=100),
    bidding_strategy=PrioritySpaceBiddingStrategy(),
    value_function=PrioritySpaceValueFunction(),
    config={"priority": 1.0}
)

# Create a stop at Fraumünster
fraumuenster = LongLatCoordinate(long=8.541375410621782, lat=47.36994730662017)
fraumuenster_stop = GridLocation("position", area.point_to_coordinate2D(fraumuenster))

# Create a random stop
random_stop = GridLocation("random")

# Create a path owner whose agents are flying from Fraumünster to a random location on the map
ownerC = WebPathOwner(
    owner_id="2",
    name="OwnerC",
    color="#1e88e5",
    stops=[fraumuenster_stop, random_stop],
    creation_ticks=[randint(0, ALLOCATION_PERIOD) for _ in range(50)],
    bidding_strategy=PriorityPathBiddingStrategy(),
    value_function=PriorityPathValueFunction(),
    near_radius=10,
    battery=10_000,
    speed=1,
    config={"priority": 0.15}
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
    name='Report Howto Demo Model',
    description='This model was generated u sing the 1_python_demo_howto.py Script',
    allocation_period=ALLOCATION_PERIOD,
)

# Generate simulation output that can be interpreted by the Visualizer
simulation_output = generate_output(simulator, simulation_time, simulation_config)

"""
Save to file
"""
with open('Prefabs/configs/1_python_demo_howto-config.json', 'w') as f:
    f.write(json.dumps(simulation_config))

with open('Prefabs/outputs/1_python_demo_howto-output.json', 'w') as f:
    f.write(json.dumps(simulation_output))
