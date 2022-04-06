from Simulator.Allocator import FCFSAllocator
from Simulator.Coordinate import TimeCoordinate
from Simulator import Simulator, Statistics, Environment, Tick
from Simulator.History import History
from owners.ABAOwner import ABAOwner
from owners.ABCOwner import ABCOwner
from owners.ABOwner import ABOwner
from owners.StationaryOwner import StationaryOwner

dimensions = TimeCoordinate(100, 100, 10, Tick(50))
environment = Environment(dimensions, [])
allocator = FCFSAllocator()
owners = [ABOwner([i for i in range(10)]), ABAOwner([i for i in range(10)]), ABCOwner([i for i in range(10)]), StationaryOwner([i for i in range(10)])]

simulator = Simulator(owners, allocator, environment)

while simulator.time_step < dimensions.t:
    # environment.visualize(simulator.time_step)
    simulator.tick()

history = History("bls", "blub", simulator)
stats = Statistics(history, allocator)
stats.non_colliding_values()
print("done")
