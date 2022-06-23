import random
from time import time_ns

from API import SimpleCoordinateType
from BiddingAllocator.BiddingABOwner import BiddingABOwner
from BiddingAllocator.BiddingAllocator import BiddingAllocator
from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator.Environment import Environment
from Simulator import Simulator, Tick
from Simulator.Generator.MapTile import MapTile
from Simulator.IO.JSONS import build_json
from Simulator.History import History
from Simulator.Owner.PathOwners.ABAOwner import ABAOwner
from Simulator.Owner.PathOwners.ABCOwner import ABCOwner
from Simulator.Owner.PathOwners.ABOwner import ABOwner
from Simulator.Owner.SpaceOwners.StationaryOwner import StationaryOwner


dimensions = TimeCoordinate(831,40,831,Tick(20))
random.seed(3)
environment = Environment(dimensions, [], [MapTile(
    [15,17161, 11475],
    dimensions,
    SimpleCoordinateType(lat=47.376034633497596, long=8.536376953124991),
    SimpleCoordinateType(lat=47.3685943521338, long=8.547363281249993)
)])
environment.init_blocker_tree()
# allocator = BiddingAllocator()
allocator = FCFSAllocator()
owners = []
for i in range(3):
    owners.append(ABCOwner("Schnabeltier"+ str(i), "red", [random.randint(0,5) for _ in range(2)]))
# owners = [BiddingABOwner("Schnabeltier", "red", [1,1,1,2], 0.5), BiddingABOwner("Schnabeltier", "red", [1,1,3,3,3], 0.7)]

history = History(dimensions, allocator, environment, owners)
SimulaterAligator = Simulator(owners, allocator, environment, history)
t0 = time_ns()
while SimulaterAligator.time_step < dimensions.t:
    # print(simulator.time_step)
    SimulaterAligator.tick()
    # SimulaterAligator.environment.visualize(SimulaterAligator.time_step)
print(f"Total: {(time_ns() - t0)/1e9}")

# res = build_json(SimulaterAligator, "test", "Schnabeltier")
# print(res)
# print("agents: ", res['statistics']['total_number_of_agents'])
# print("cols: ", res['statistics']['total_number_of_collisions'])
# print("wf: ", res['statistics']['total_achieved_welfare'])
print("done")
