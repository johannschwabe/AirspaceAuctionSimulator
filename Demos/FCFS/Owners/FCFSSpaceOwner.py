from Simulator import SpaceOwner, SpaceAgent
from ..BiddingStrategy.FCFSSpaceBiddingStrategy import FCFSSpaceBiddingStrategy


class FCFSSpaceOwner(SpaceOwner):
    label = "FCFS Space Owner"
    description = "FCFS Space Owner"

    def __init__(self, owner_id, name, color, stops, creation_ticks, size):
        super().__init__(owner_id, name, color, stops, creation_ticks, size)

    def initialize_agent(self, blocks):
        agent_id: str = self.get_agent_id()
        bidding_strategy: "FCFSSpaceBiddingStrategy" = FCFSSpaceBiddingStrategy()
        return SpaceAgent(agent_id, bidding_strategy, blocks)
