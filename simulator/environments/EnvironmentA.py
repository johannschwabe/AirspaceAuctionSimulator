from simulator.coordinates import Coordinate
from simulator.environments.Environment import Environment


class EnvironmentA(Environment):
    def __init__(self, dimension: Coordinate):
        super().__init__(dimension, [])
