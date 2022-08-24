from Simulator import PathOwner
from ..Agents.FCFSPathAgent import FCFSPathAgent


class FCFSPathOwner(PathOwner):
    label = "FCFS Path Owner"
    description = "FCFS Path Owner"

    def __init__(self, owner_id, name, color, stops, creation_ticks):
        super().__init__(owner_id, name, color, stops, creation_ticks)

    def initialize_agent(self, locations, stays, simulator, speed, battery, near_radius):
        return FCFSPathAgent(locations, stays, simulator, speed=speed, battery=battery, near_radius=near_radius)
