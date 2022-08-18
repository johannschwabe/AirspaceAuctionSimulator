from AAS import ABAOwner
from Demos.FCFS.Agents.FCFSABAAgent import FCFSABAAgent


class FCFSABAOwner(ABAOwner):
    label = "FCFS A to B to A"
    description = "Owners with agents going from A to B and back to A"

    def __init__(self, name, color, stops, creation_ticks):
        super().__init__(name, color, stops, creation_ticks)

    def initialize_agent(self, start, target, simulator, speed, battery, stay):
        return FCFSABAAgent(start, target, simulator, speed=speed, battery=battery, stay=stay)