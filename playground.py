import random
from time import time_ns

from BiddingAllocator.BiddingABOwner import BiddingABOwner
from BiddingAllocator.BiddingAllocator import BiddingAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator.Environment import Environment
from Simulator import Simulator, Tick
from Simulator.IO.JSONS import build_json
from Simulator.History import History

dimensions = TimeCoordinate(30, 30, 1, Tick(60))
random.seed(3)
environment = Environment(dimensions, [])
allocator = BiddingAllocator()
owners = []
for i in range(7):
    owners.append(BiddingABOwner("Schnabeltier"+ str(i), "red", [random.randint(0,8) for _ in range(random.randint(2,8))], random.random()))
# owners = [BiddingABOwner("Schnabeltier", "red", [1,1,1,2], 0.5), BiddingABOwner("Schnabeltier", "red", [1,1,3,3,3], 0.7)]

history = History(dimensions, allocator, environment, owners)
simulator = Simulator(owners, allocator, environment, history)
t0 = time_ns()
while simulator.time_step < dimensions.t:
    # print(simulator.time_step)
    simulator.tick()
    simulator.environment.visualize(simulator.time_step)
print(f"Total: {(time_ns() - t0)/1e9}")

res = build_json(simulator, "test", "Schnabeltier")
print(res)
print("agents: ", res['statistics']['total_number_of_agents'])
print("cols: ", res['statistics']['total_number_of_collisions'])
print("wf: ", res['statistics']['total_achieved_welfare'])
print("done")
