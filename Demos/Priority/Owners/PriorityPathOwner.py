from Demos.Priority.Agents.PriorityPathAgent import PriorityPathAgent
from Simulator import PathOwner


class PriorityPathOwner(PathOwner):
    label = "Path"
    description = "Path"

    def __init__(self, owner_id, name, color, stops, creation_ticks, priority):
        super().__init__(owner_id, name, color, stops, creation_ticks)
        self.priority = priority

    def initialize_agent(self, locations, stays, simulator, speed, battery, near_radius):
        return PriorityPathAgent(locations, self.priority, simulator, stays, speed=speed, battery=battery,
                                 near_radius=near_radius)
