from Simulator import Agent, PointOfInterest
from Simulator.Coordinate import TimeCoordinate


class AToBAgent(Agent):
    def __init__(self, a: TimeCoordinate, b: TimeCoordinate, value: float = 100):
        desired_path = [PointOfInterest(a, a.t), PointOfInterest(b, b.t)]
        super().__init__(value, desired_path)
