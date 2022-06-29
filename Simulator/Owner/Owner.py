import random
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

from ..Agent import Agent
from ..Coordinate import TimeCoordinate
from ..Environment import Environment

if TYPE_CHECKING:
    from .. import Tick


class Owner(ABC):
    _id: int = 10000

    def __init__(self, name: str, color: str):
        self.name: str = name
        self.color: str = color
        self.agents: List[Agent] = []
        self.total_achieved_welfare: float = 0.
        self.total_optimal_welfare: float = 0.
        self.total_costs: float = 0.
        self.id: int = Owner._id
        Owner._id += 1

    @abstractmethod
    def generate_agents(self, t: int, env: Environment) -> List[Agent]:
        pass

    @staticmethod
    def valid_random_coordinate(env: Environment, t: "Tick", near_radius: int, speed: int):
        dimensions = env._dimension
        coord = TimeCoordinate(random.randint(0, dimensions.x - 1),
                               0,
                               random.randint(0, dimensions.z - 1),
                               t)
        while True:
            if not env.is_blocked(coord, near_radius, speed):
                break
            coord.y += 1
            if coord.y >= env.get_dim().y:
                coord = TimeCoordinate(random.randint(0, dimensions.x - 1),
                                       0,
                                       random.randint(0, dimensions.z - 1),
                                       t)
        return coord
