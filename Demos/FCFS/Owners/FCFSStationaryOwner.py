from Demos.FCFS.Agents.FCFSStationaryAgent import FCFSStationaryAgent
from Simulator import StationaryOwner


class FCFSStationaryOwner(StationaryOwner):
    label = "FCFS Stationary Owners"
    description = "An owner interested in a set of stationary cubes"

    def __init__(self, owner_id, name, color, stops, creation_ticks, size):
        super().__init__(owner_id, name, color, stops, creation_ticks, size)

    def initialize_agent(self, simulator, blocks):
        return FCFSStationaryAgent(blocks, simulator)
