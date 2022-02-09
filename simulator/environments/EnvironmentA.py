from simulator.coordinates.Coordinates import Coordinates
from simulator.environments.Environment import Environment


class EnvironmentA(Environment):
    def __init__(self, dimension: Coordinates):
        super().__init__(dimension, [])
