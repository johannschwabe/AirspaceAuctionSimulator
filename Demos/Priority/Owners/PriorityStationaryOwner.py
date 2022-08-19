from Simulator import StationaryOwner
from Demos.Priority.Agents.PriorityStationaryAgent import PriorityStationaryAgent


class PriorityStationaryOwner(StationaryOwner):
    label = "Priority Stationary"
    description = "A priority owner interested in a set of cubes"

    def __init__(self,
                 name,
                 color,
                 stops,
                 creation_ticks,
                 size,
                 priority):
        super().__init__(name, color, stops, creation_ticks, size)
        self.priority = priority

    def initialize_agent(self, simulator, blocks):
        return PriorityStationaryAgent(blocks, simulator, self.priority)
