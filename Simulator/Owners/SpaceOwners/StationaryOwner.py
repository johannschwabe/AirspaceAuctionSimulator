import random
from typing import List, TYPE_CHECKING

from Simulator.Agents.SpaceAgents.StationaryAgent import StationaryAgent
from ..SpaceOwner import SpaceOwner
from ...Coordinates.Coordinate4D import Coordinate4D

if TYPE_CHECKING:
    from ..GridLocation import GridLocation
    from ...Simulator import Simulator
    from Simulator.Agents.SpaceAgents.StationaryAgent import StationaryAgent


class StationaryOwner(SpaceOwner):
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

    def __init__(self, name: str, color: str, stops: List["GridLocation"], creation_ticks: List[int],
                 size: "Coordinate4D" = Coordinate4D(5, 5, 5, 5)):
        super().__init__(name, color, stops)
        self.creation_ticks = creation_ticks
        self.size: "Coordinate4D" = size

    def initialize_agent(self, simulator: "Simulator", blocks: List[List["Coordinate4D"]]) -> StationaryAgent:
        pass

    def generate_agents(self, t: int, simulator: "Simulator") -> List["StationaryAgent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            blocks = []
            for stop in self.stops:
                bottom_left = self.generate_stop_coordinates(stop, simulator.environment, t, self.size)
                top_right = bottom_left + self.size
                blocks.append([bottom_left, top_right])
            agent = self.initialize_agent(simulator, blocks)
            res.append(agent)
            print(f"Stationary created {agent}")

        self.agents += res
        return res
