from Demos.FCFS.Agents.FCFSPathAgent import FCFSPathAgent
from Simulator import PathOwner


class FCFSPathOwner(PathOwner):
    label = "Path"
    description = "Path"

    def __init__(self, owner_id, name, color, stops, creation_ticks):
        super().__init__(owner_id, name, color, stops, creation_ticks)

    def initialize_agent(self, locations, stays, simulator, speed, battery, near_radius):
        return FCFSPathAgent(locations, stays, simulator, speed=speed, battery=battery, near_radius=near_radius)
