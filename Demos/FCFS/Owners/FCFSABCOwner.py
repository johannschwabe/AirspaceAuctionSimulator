from Demos.FCFS.Agents.FCFSABCAgent import FCFSABCAgent
from Simulator import ABCOwner


class FCFSABCOwner(ABCOwner):
    label = "FCFS A to B to C"
    description = "A owner with agents going from A to a number of stops"

    def __init__(self, owner_id, name, color, stops, creation_ticks):
        super().__init__(owner_id, name, color, stops, creation_ticks)

    def initialize_agent(self, locations, stays, simulator, speed, battery, near_radius):
        return FCFSABCAgent(locations, stays, simulator, speed=speed, battery=battery, near_radius=near_radius)
