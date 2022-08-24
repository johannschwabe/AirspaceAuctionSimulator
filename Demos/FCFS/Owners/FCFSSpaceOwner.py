from Simulator import SpaceOwner, Coordinate4D
from ..Agents.FCFSSpaceAgent import FCFSSpaceAgent


class FCFSSpaceOwner(SpaceOwner):
    label = "FCFS Space Owner"
    description = "FCFS Space Owner"

    def __init__(self, owner_id, name, color, stops, creation_ticks, size=Coordinate4D(20, 20, 20, 200)):
        super().__init__(owner_id, name, color, stops, creation_ticks, size)

    def initialize_agent(self, simulator, blocks):
        return FCFSSpaceAgent(blocks, simulator)
