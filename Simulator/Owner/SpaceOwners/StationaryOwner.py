import random
from typing import List, TYPE_CHECKING

from Simulator.Coordinate import Coordinate3D, Coordinate4D
from Simulator.Owner.SpaceOwner import SpaceOwner
from Simulator.Agent import StationaryAgent

if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Agent import Agent
    from Simulator.Owner import GridLocation


class StationaryOwner(SpaceOwner):
    label = "Stationary Owner"
    description = "An owner interested in a set of stationary cubes"
    positions = ">0"
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

    def __init__(self, name: str, color: str, stops: List["GridLocation"], creation_ticks: List[int],
                 size: "Coordinate4D" = Coordinate4D(5, 5, 5, 5)):
        super().__init__(name, color, stops)
        self.creation_ticks = creation_ticks
        self.size: "Coordinate4D" = size

    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            blocks = []
            for stop in self.stops:
                bottom_left = self.generate_stop_coordinates(stop, env, t, self.size)
                top_right = bottom_left + self.size
                blocks.append([bottom_left, top_right])
            agent = StationaryAgent(blocks)
            res.append(agent)
            print(f"Stationary created {agent}")

        self.agents += res
        return res
