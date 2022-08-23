import random

from Demos.Priority.Agents.PrioritySpaceAgent import PrioritySpaceAgent
from Simulator import SpaceOwner, Coordinate4D


class PrioritySpaceOwner(SpaceOwner):
    label = "Space"
    description = "Space"

    def __init__(self, owner_id, name, color, stops, creation_ticks, size=Coordinate4D(20, 20, 20, 200),
                 priority=random.random()):
        super().__init__(owner_id, name, color, stops, creation_ticks, size)
        self.priority = priority

    def initialize_agent(self, simulator, blocks):
        return PrioritySpaceAgent(blocks, self.priority, simulator)
