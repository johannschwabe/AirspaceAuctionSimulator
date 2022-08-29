from Demos.FCFS.Bids.FCFSPathBid import FCFSPathBid
from Simulator.Agents.AgentType import AgentType
from Simulator.Agents.PathAgent import PathAgent
from Simulator.Bids.BiddingStrategy import BiddingStrategy
from Simulator.Environment.Environment import Environment


class FCFSPathBiddingStrategy(BiddingStrategy):
    label = "FCFS Path Bidding Strategy"
    description = "An Bidding Strategy for FCFS Path Agents"
    min_locations = 2
    max_locations = 5
    meta = []
    allocation_type = AgentType.PATH.value

    def generate_bid(self, agent: PathAgent, _environment: Environment, _time_step: int) -> FCFSPathBid:
        return FCFSPathBid(agent)
