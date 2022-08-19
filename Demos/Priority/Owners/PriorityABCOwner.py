from Simulator import ABCOwner
from Demos.Priority.Agents.PriorityABCAgent import PriorityABCAgent


class PriorityABCOwner(ABCOwner):
    label = "Priority A to B to A"
    description = "Owners with agents going from A to B and back to A"

    def __init__(self, name, color, stops, creation_ticks, priority):
        super().__init__(name, color, stops, creation_ticks)
        self.priority = priority

    def initialize_agent(self, locations, stays, simulator, speed, battery):
        return PriorityABCAgent(locations, self.priority, simulator, stays, speed=speed, battery=battery)
