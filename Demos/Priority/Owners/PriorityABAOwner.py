from Demos.Priority.Agents.PriorityABAAgent import PriorityABAAgent
from Simulator import ABAOwner


class PriorityABAOwner(ABAOwner):
    label = "Priority A to B to A"
    description = "Owners with agents going from A to B and back to A"

    def __init__(self, name, color, stops, creation_ticks, priority):
        super().__init__(name, color, stops, creation_ticks)
        self.priority = priority

    def initialize_agent(self, start, target, simulator, speed, battery, stay, near_radius):
        return PriorityABAAgent(start, target, self.priority, simulator, stay, speed=speed, battery=battery,
                                near_radius=near_radius)
