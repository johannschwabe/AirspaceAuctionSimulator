from Simulator import ABOwner
from Demos.Priority.Agents.PriorityABAgent import PriorityABAgent


class PriorityABOwner(ABOwner):
    label = "Priority A to B"
    description = "A priority owner with a priority going from A to B"

    def __init__(self, name, color, stops, creation_ticks, priority):
        super().__init__(name, color, stops, creation_ticks)
        self.priority = priority

    def initialize_agent(self, start, target, simulator, speed, battery):
        return PriorityABAgent(start, target, self.priority, simulator, speed=speed, battery=battery)
