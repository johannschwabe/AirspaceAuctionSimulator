from Simulator.Coordinate import TimeCoordinate
from Simulator.Time import Tick
from Simulator.History import Generator

dimensions = TimeCoordinate(20, 20, 20, Tick(50))
g = Generator(agents=100, owners=5, dimensions=dimensions, avg_flight_time=50)
g.simulate()
history = g.history
print(history.json())