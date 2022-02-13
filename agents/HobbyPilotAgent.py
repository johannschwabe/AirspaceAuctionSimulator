from Simulator import Agent, PointOfInterest, Tick
from Simulator.Coordinate import Coordinate


class HobbyPilotAgent(Agent):
    def __init__(self, corner1: Coordinate, corner2: Coordinate, t_start: int, t_stop: int, value: float = 100):
        assert corner1 <= corner2
        assert t_start <= t_stop

        desired_path = []
        for t in range(t_start, t_stop + 1):
            for x in range(corner1.x, corner2.x + 1):
                for y in range(corner1.y, corner2.y + 1):
                    for z in range(corner1.z, corner2.z + 1):
                        desired_path.append(PointOfInterest(Coordinate(x, y, z), Tick(t)))

        super().__init__(value, desired_path)
