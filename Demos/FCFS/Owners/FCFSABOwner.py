from Simulator import ABOwner
from Demos.FCFS.Agents.FCFSABAgent import FCFSABAgent


class FCFSABOwner(ABOwner):
    label = "FCFS A to B"
    description = "Owners with agents going from A to B"

    def __init__(self, name, color, stops, creation_ticks):
        super().__init__(name, color, stops, creation_ticks)

    def initialize_agent(self, start, target, simulator, speed, battery):
        return FCFSABAgent(start, target, simulator, speed=speed, battery=battery)
