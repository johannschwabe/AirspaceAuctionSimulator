from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator.Environment import Environment
from Simulator import Simulator, Statistics, Tick
from Simulator.History import History
from Simulator.History2 import History2
from Simulator.Owner.ABOwner import ABOwner
from time import time_ns
import random


random.seed(2)
dimensions = TimeCoordinate(50, 50, 50, Tick(150))
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
owners = [ABOwner(list(range(50)))]

history = History2(dimensions, allocator, environment, owners)
simulator = Simulator(owners, allocator, environment, history)
t0 = time_ns()

times = []

while simulator.time_step < dimensions.t:
    # environment.visualize(simulator.time_step)
    a = time_ns()
    simulator.tick()
    times.append(time_ns() - a)
    print(f"{simulator.time_step}: {(time_ns() - a)/1e9}")
print(f"Total: {(time_ns() - t0)/1e9}")
history = History("bls", "blub", simulator)
stats = Statistics(simulator)
stats.non_colliding_values()
# cols, nfc, nfi, ffc, ffi = stats.close_passings()
stats.average_owners_welfare()
stats.average_agents_welfare()

print(times)
