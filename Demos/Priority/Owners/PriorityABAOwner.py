from Simulator import ABAOwner
from Demos.Priority.Agents.PriorityABAAgent import PriorityABAAgent


class PriorityABAOwner(ABAOwner):
    label = "Priority A to B to A"
    description = "Owners with agents going from A to B and back to A"

    def __init__(self, name, color, stops, creation_ticks, priority):
        super().__init__(name, color, stops, creation_ticks)
        self.priority = priority

    def initialize_agent(self, start, target, simulator, speed, battery, stay):
        return PriorityABAAgent(start, target, self.priority, simulator, stay, speed=speed, battery=battery)
