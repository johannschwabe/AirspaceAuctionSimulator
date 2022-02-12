from simulator.coordinates import Coordinate
from simulator.environments.Environment import Environment


class EnvironmentA(Environment):
    def __init__(self, dimension: Coordinate):
        super().__init__(dimension, [])

    def clone(self):
        new_env = EnvironmentA(self.dimension)
        new_env.relevant_fields = self.relevant_fields
        new_env.agents = self.agents
        return new_env