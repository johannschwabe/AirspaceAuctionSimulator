from typing import List, Dict

from Simulator import Agent, PointOfInterest, Tick
from Simulator.Coordinate import Coordinate


class HobbyPilotAgent(Agent):
    def __init__(self, corner1: Coordinate, corner2: Coordinate, t_start: int, t_stop: int, value: float = 100):
        assert corner1 <= corner2
        assert t_start <= t_stop

        points_of_interest = []
        for t in range(t_start, t_stop + 1):
            for x in range(corner1.x, corner2.x + 1):
                for y in range(corner1.y, corner2.y + 1):
                    for z in range(corner1.z, corner2.z + 1):
                        points_of_interest.append(PointOfInterest(Coordinate(x, y, z), Tick(t)))

        super().__init__(value, points_of_interest)

    def calculate_desired_path(self, costs: Dict[str, float] = None) -> List[PointOfInterest]:
        desired_path = self.points_of_interest
        if costs is not None:
            desired_path = list(filter(lambda poi: not poi.to_time_coordinate().get_key() in costs, desired_path))

        desired_path.sort(key=lambda x: x.tick)
        return desired_path
