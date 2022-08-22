from Demos.Priority.Agents.PriorityStationaryAgent import PriorityStationaryAgent
from Simulator import StationaryOwner


class PriorityStationaryOwner(StationaryOwner):
    label = "Priority Stationary"
    description = "A priority owner interested in a set of cubes"

    def __init__(self, owner_id, name, color, stops, creation_ticks, size, priority):
        super().__init__(owner_id, name, color, stops, creation_ticks, size)
        self.priority = priority

    def initialize_agent(self, simulator, blocks):
        return PriorityStationaryAgent(blocks, simulator, self.priority)
