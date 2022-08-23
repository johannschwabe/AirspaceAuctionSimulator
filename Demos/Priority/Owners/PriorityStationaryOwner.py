import random

from Demos.Priority.Agents.PriorityStationaryAgent import PriorityStationaryAgent
from Simulator import StationaryOwner, Coordinate4D


class PriorityStationaryOwner(StationaryOwner):
    label = "Priority Stationary"
    description = "A priority owner interested in a set of cubes"

    def __init__(self, owner_id, name, color, stops, creation_ticks, size=Coordinate4D(20, 20, 20, 200),
                 priority=random.random()):
        super().__init__(owner_id, name, color, stops, creation_ticks, size)
        self.priority = priority

    def initialize_agent(self, simulator, blocks):
        return PriorityStationaryAgent(blocks, self.priority, simulator)
