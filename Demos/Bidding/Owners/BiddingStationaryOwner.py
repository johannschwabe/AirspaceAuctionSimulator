import random
from typing import List, TYPE_CHECKING

from Demos.Bidding.Allocator.BiddingAllocator import BiddingStationaryAgent
from AAS import Environment
from AAS.Coordinates import Coordinate4D
from AAS.Owner.SpaceOwners.StationaryOwner import StationaryOwner

if TYPE_CHECKING:
    from AAS.Owner import GridLocation


class BiddingStationaryOwner(StationaryOwner):
    label = "Bidding Stationary"
    description = "A bidding owner interested in a set of cubes"
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
                 name: str,
                 color: str,
                 stops: List["GridLocation"],
                 creation_ticks: List[int],
                 size: "Coordinate4D" = Coordinate4D(5, 5, 5, 5),
                 priority: float = None):
        super().__init__(name, color, stops, creation_ticks, size)
        self.priority = priority if priority else random.random() * 10

    def generate_agents(self, t: int, env: "Environment") -> List["Agents"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            blocks = []
            for stop in self.stops:
                bottom_left = self.generate_stop_coordinates(stop, env, t, self.size)
                top_right = bottom_left + self.size
                blocks.append([bottom_left, top_right])
            agent = BiddingStationaryAgent(blocks, self.priority)
            res.append(agent)
            print(f"Bidding Stationary created {agent}")

        self.agents += res
        return res
