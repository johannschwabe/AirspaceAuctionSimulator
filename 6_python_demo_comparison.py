import json
import random
from random import randint
from time import time_ns

from API import Area, APIWorldCoordinates, EnvironmentGen, MapTile, LongLatCoordinate, WebPathOwner, \
    WebSpaceOwner, GridLocation, generate_config, generate_output
from API.GridLocation.Heatmap import SparseHeatmap
from Demos.FCFS import FCFSAllocator, FCFSPathValueFunction, FCFSSpaceValueFunction
from Demos.FCFS.BiddingStrategy.FCFSPathBiddingStrategy import FCFSPathBiddingStrategy
from Demos.FCFS.BiddingStrategy.FCFSSpaceBiddingStrategy import FCFSSpaceBiddingStrategy
from Demos.FCFS.PaymentRule.FCFSPaymentRule import FCFSPaymentRule
from Demos.Priority import PriorityAllocator, PriorityPaymentRule, PriorityPathBiddingStrategy, \
    PriorityPathValueFunction, PrioritySpaceBiddingStrategy, PrioritySpaceValueFunction
from Simulator import Simulator, Coordinate4D, Mechanism

random.seed(3)

TIMESTEPS = 4000
ALLOCATION_PERIOD = 1000

# Specifies a point in Bern, Switzerland
coordinate = APIWorldCoordinates(long=7.453635943195272, lat=46.948296530129056)

# Resolves open-streetmap tiles around specified coordinate in Bern
maptiles = MapTile.tiles_from_coordinates(coordinate, neighbouring_tiles=1)

# Bounding-Box spanned by zurich tile, which is needed to determine the size of our playing area
bottom_left_coordinate = APIWorldCoordinates(long=7.4461710774213765, lat=46.944598524881215)
top_right_coordinate = APIWorldCoordinates(long=7.4597055113035795, lat=46.95118625428702)

# Defines 2D area using both coordinates and given resolution (meters per voxel)
area = Area(bottom_left_coordinate, top_right_coordinate)

# Use area to find out play field resolution in voxels
[x, z] = area.dimension
y = 100  # Set map height to 100 voxels (which is also 50 meters since we have not specified a resolution)

allocators = [FCFSAllocator, PriorityAllocator]
payment_rules = [FCFSPaymentRule, PriorityPaymentRule]
path_bidding_strategies = [FCFSPathBiddingStrategy, PriorityPathBiddingStrategy]
space_bidding_strategies = [FCFSSpaceBiddingStrategy, PrioritySpaceBiddingStrategy]
path_value_functions = [FCFSPathValueFunction, PriorityPathValueFunction]
space_value_functions = [FCFSSpaceValueFunction, PrioritySpaceValueFunction]

owner_a_ticks = [randint(0, ALLOCATION_PERIOD) for _ in range(10)]
owner_b_ticks = [randint(0, ALLOCATION_PERIOD) for _ in range(10)]
owner_c_ticks = [0, 0, 0, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800, 800, 900, 900]

for i in range(len(allocators)):
    # Define environment
    environment_generator = EnvironmentGen(
        dimensions=Coordinate4D(x, y, z, t=TIMESTEPS),
        maptiles=maptiles,
        map_area=area,
    )

    # Choose allocator, compatible payment rule and compatible mechanism
    allocator = allocators[i]()
    payment_rule = payment_rules[i]()
    mechanism = Mechanism(allocator, payment_rule)

    # Define owners that participate in simulation
    ownerA = WebPathOwner(
        owner_id="0",
        name="OwnerA",
        color="#e53935",
        stops=[
            GridLocation("position",
                         area.point_to_coordinate2D(LongLatCoordinate(long=7.448472707397318, lat=46.94813991133983))),
            GridLocation("random"),
        ],
        creation_ticks=owner_a_ticks,
        bidding_strategy=path_bidding_strategies[i](),
        value_function=path_value_functions[i](),
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
                         area.point_to_coordinate2D(LongLatCoordinate(long=7.451935684146172, lat=46.9469169118693))),
            GridLocation("random"),
        ],
        creation_ticks=owner_b_ticks,
        bidding_strategy=path_bidding_strategies[i](),
        value_function=path_value_functions[i](),
        near_radius=10,
        battery=5000,
        speed=1,
        config={"priority": 0.3}
    )

    ownerC = WebSpaceOwner(
        owner_id="2",
        name="OwnerB",
        color="#1e88e5",
        stops=[GridLocation("heatmap", heatmap=SparseHeatmap({
            area.point_to_coordinate2D(LongLatCoordinate(long=7.448352457867829, lat=46.948238408893694)): 0.2,
            area.point_to_coordinate2D(LongLatCoordinate(long=7.455951717980163, lat=46.94747502165524)): 0.5,
            area.point_to_coordinate2D(LongLatCoordinate(long=7.451526856162293, lat=46.94823846841664)): 0.3,
            area.point_to_coordinate2D(LongLatCoordinate(long=7.449915676605629, lat=46.946629594776915)): 0.3,
            area.point_to_coordinate2D(LongLatCoordinate(long=7.454617124101731, lat=46.94914958099759)): 0.2,
        }))],
        creation_ticks=owner_c_ticks,
        size=Coordinate4D(x=15, y=50, z=15, t=100),
        bidding_strategy=space_bidding_strategies[i](),
        value_function=space_value_functions[i](),
        config={"priority": 1.0}
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
        name=f'Report Comparison Model {allocator.__class__.__name__}',
        description='This model was generated using the 6_python_demo_comparison.py Script',
        allocation_period=ALLOCATION_PERIOD,
    )

    # Generate simulation output that can be interpreted by API
    simulation_output = generate_output(simulator, simulation_time, simulation_config)

    with open(f'./Prefabs/configs/6_python_demo_comparison_{allocator.__class__.__name__.lower()}-config.json',
              'w') as f:
        f.write(json.dumps(simulation_config))

    with open(f'./Prefabs/outputs/6_python_demo_comparison_{allocator.__class__.__name__.lower()}-output.json',
              'w') as f:
        f.write(json.dumps(simulation_output))

    print("********************************")
    print(f"Utility of {allocator.__class__.__name__}: {simulation_output['statistics']['utility_stats']['total']}")
    print(f"Value of {allocator.__class__.__name__}: {simulation_output['statistics']['value_stats']['total']}")
    print(f"Payment of {allocator.__class__.__name__}: {simulation_output['statistics']['payment_stats']['total']}")
    print("********************************")
