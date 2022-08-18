import random

from AAS import StationaryOwner, Coordinate4D


class PriorityStationaryOwner(StationaryOwner):
    label = "Priority Stationary"
    description = "A priority owner interested in a set of cubes"

    def __init__(self,
                 name,
                 color,
                 stops,
                 creation_ticks,
                 size=Coordinate4D(5, 5, 5, 5),
                 priority=None):
        super().__init__(name, color, stops, creation_ticks, size)
        self.priority = priority if priority else random.random() * 10
