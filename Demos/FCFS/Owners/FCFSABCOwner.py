from Simulator import ABCOwner
from Demos.FCFS.Agents.FCFSABCAgent import FCFSABCAgent


class FCFSABCOwner(ABCOwner):
    label = "FCFS A to B to C"
    description = "A owner with agents going from A to a number of stops"

    def __init__(self, name, color, stops, creation_ticks):
        super().__init__(name, color, stops, creation_ticks)

    def initialize_agent(self, locations, stays, simulator, speed, battery):
        return FCFSABCAgent(locations, stays, simulator, speed=speed, battery=battery)
