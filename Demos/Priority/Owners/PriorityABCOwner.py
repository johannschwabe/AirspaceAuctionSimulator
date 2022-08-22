from Demos.Priority.Agents.PriorityABCAgent import PriorityABCAgent
from Simulator import ABCOwner


class PriorityABCOwner(ABCOwner):
    label = "Priority A to B to A"
    description = "Owners with agents going from A to B and back to A"

    def __init__(self, name, color, stops, creation_ticks, priority):
        super().__init__(name, color, stops, creation_ticks)
        self.priority = priority

    def initialize_agent(self, locations, stays, simulator, speed, battery, near_radius):
        return PriorityABCAgent(locations, self.priority, simulator, stays, speed=speed, battery=battery,
                                near_radius=near_radius)
