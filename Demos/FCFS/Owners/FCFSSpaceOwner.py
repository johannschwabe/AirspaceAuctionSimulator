from Simulator import SpaceOwner, Coordinate4D, SpaceAgent
from ..BiddingStrategy.FCFSSpaceBiddingStrategy import FCFSSpaceBiddingStrategy
from ..ValueFunction.FCFSSpaceValueFunction import FCFSSpaceValueFunction


class FCFSSpaceOwner(SpaceOwner):
    label = "FCFS Space Owner"
    description = "FCFS Space Owner"

    def __init__(self, owner_id, name, color, stops, creation_ticks, size=Coordinate4D(20, 20, 20, 200)):
        super().__init__(owner_id, name, color, stops, creation_ticks, size)

    def initialize_agent(self, blocks):
        agent_id: str = self.get_agent_id()
        bidding_strategy: "FCFSSpaceBiddingStrategy" = FCFSSpaceBiddingStrategy()
        value_function = FCFSSpaceValueFunction()
        return SpaceAgent(agent_id, bidding_strategy, value_function, blocks)
