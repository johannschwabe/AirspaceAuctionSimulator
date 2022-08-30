from Simulator import PathOwner, PathAgent
from ..BiddingStrategy.FCFSPathBiddingStrategy import FCFSPathBiddingStrategy


class FCFSPathOwner(PathOwner):
    label = "FCFS Path Owner"
    description = "FCFS Path Owner"

    def __init__(self, owner_id, name, color, stops, creation_ticks):
        super().__init__(owner_id, name, color, stops, creation_ticks)

    def initialize_agent(self, locations, stays, speed, battery, near_radius):
        agent_id: str = self.get_agent_id()
        bidding_strategy: "FCFSPathBiddingStrategy" = FCFSPathBiddingStrategy()
        return PathAgent(agent_id, bidding_strategy, locations, stays, speed=speed, battery=battery,
                         near_radius=near_radius)
