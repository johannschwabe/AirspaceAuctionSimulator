from Simulator import PathOwner
from ..Agents.FCFSPathAgent import FCFSPathAgent


class FCFSPathOwner(PathOwner):
    label = "FCFS Path Owner"
    description = "FCFS Path Owner"

    def __init__(self, owner_id, name, color, stops, creation_ticks):
        super().__init__(owner_id, name, color, stops, creation_ticks)

    def initialize_agent(self, locations, stays, speed, battery, near_radius):
        agent_id: str = self.get_agent_id()
        return FCFSPathAgent(agent_id, locations, stays, speed=speed, battery=battery, near_radius=near_radius)
