from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator import Simulator, Statistics, Environment, Tick
from Simulator.History import History
from owners.ABOwner import ABOwner

dimensions = TimeCoordinate(20, 20, 1, Tick(250))
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
owners = [ABOwner([i for i in range(10)])]

simulator = Simulator(owners, allocator, environment)

while simulator.time_step < dimensions.t:
    environment.visualize(simulator.time_step)
    simulator.tick()

history = History("bls", "blub", simulator)
stats = Statistics(history, allocator)
stats.non_colliding_values()
print("done")
