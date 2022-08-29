import random
from abc import ABC
from typing import List, TYPE_CHECKING

from .Owner import Owner
from ..Agents.AgentType import AgentType

if TYPE_CHECKING:
    from ..Location.GridLocation import GridLocation
    from ..Environment.Environment import Environment
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Agents.SpaceAgent import SpaceAgent


class SpaceOwner(Owner, ABC):
    allocation_type: str = AgentType.SPACE.value
    min_locations = 1
    max_locations = 100
    meta = [
        {
            "key": "size_x",
            "label": "Field Size X",
            "description": "Size of reserved field in X-Dimension",
            "type": "int",
            "value": random.randint(0, 100)
        },
        {
            "key": "size_y",
            "label": "Field Size Y",
            "description": "Size of reserved field in Y-Dimension",
            "type": "int",
            "value": random.randint(0, 100)
        },
        {
            "key": "size_z",
            "label": "Field Size Z",
            "description": "Size of reserved field in Z-Dimension",
            "type": "int",
            "value": random.randint(0, 100)
        },
        {
            "key": "size_t",
            "label": "Reservation Duration",
            "description": "Number of ticks field should be reserved",
            "type": "int",
            "value": random.randint(0, 100)
        }
    ]

    def __init__(self,
                 owner_id: str,
                 name: str,
                 color: str,
                 stops: List["GridLocation"],
                 creation_ticks: List[int],
                 size: "Coordinate4D"):
        super().__init__(owner_id, name, color)
        self.stops = stops
        self.creation_ticks = creation_ticks
        self.size: "Coordinate4D" = size

    @staticmethod
    def generate_stop_coordinates(stop: "GridLocation", env: "Environment", t: int) -> "Coordinate4D":
        coord = stop.generate_coordinates(env, t + 1)
        return coord

    def initialize_agent(self, blocks: List[List["Coordinate4D"]]) -> "SpaceAgent":
        pass

    def generate_agents(self, t: int, environment: "Environment") -> List["SpaceAgent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            blocks = []
            for stop in self.stops:
                center = self.generate_stop_coordinates(stop, environment, t)
                bottom_left = center.clone()
                bottom_left.x -= round(self.size.x / 2)
                bottom_left.z -= round(self.size.z / 2)
                top_right = bottom_left + self.size
                blocks.append([bottom_left, top_right])
            agent = self.initialize_agent(blocks)
            res.append(agent)
            print(f"{agent} {', '.join([str(block) for block in blocks])}")

        self.agents += res
        return res
