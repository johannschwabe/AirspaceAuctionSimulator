from Demos.FCFS.Bids.FCFSPathBid import FCFSPathBid
from Simulator.Agents.PathAgent import PathAgent
from Simulator.Bids.BiddingStrategy import BiddingStrategy
from Simulator.Environment.Environment import Environment


class FCFSPathBiddingStrategy(BiddingStrategy):
    def generate_bid(self, agent: PathAgent, _environment: Environment, _time_step: int) -> FCFSPathBid:
        return FCFSPathBid(agent)
