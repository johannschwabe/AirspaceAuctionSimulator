from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator.Environment import Environment
from Simulator import Simulator, Statistics, Tick
from Simulator.History import History
from Simulator.History2 import History2
from owners.ABOwner import ABOwner

dimensions = TimeCoordinate(10, 10, 1, Tick(250))
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
owners = [ABOwner([0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 3, 4, 5, 10, 20, 20])]

history = History2(dimensions, allocator, environment, owners)
simulator = Simulator(owners, allocator, environment, history)

while simulator.time_step < dimensions.t:
    environment.visualize(simulator.time_step)
    simulator.tick()

history = History("bls", "blub", simulator)
stats = Statistics(history, allocator)
stats.non_colliding_values()
stats.close_passings()
stats.average_owners_welfare()
stats.average_agents_welfare()
print("done")
