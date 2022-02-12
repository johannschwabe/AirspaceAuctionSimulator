from ..Coordinate import Coordinate
from .Environment import Environment


class EnvironmentA(Environment):
    def __init__(self, dimension: Coordinate):
        super().__init__(dimension, [])
