import random
from typing import List, TYPE_CHECKING

from AAS.Coordinates import Coordinate4D
from AAS.Owners.SpaceOwner import SpaceOwner

if TYPE_CHECKING:
    from AAS.Owners import GridLocation


class FCFSStationaryOwner(SpaceOwner):
    label = "Stationary Owners"
    description = "An owner interested in a set of stationary cubes"
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
