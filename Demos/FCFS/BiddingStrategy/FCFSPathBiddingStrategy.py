from Simulator import BiddingStrategy, PathAgent, Environment
from ..Bids.FCFSPathBid import FCFSPathBid


class FCFSPathBiddingStrategy(BiddingStrategy):
    def generate_bid(self, agent: "PathAgent", _environment: "Environment", _time_step: int) -> "FCFSPathBid":
        return FCFSPathBid(agent, agent.locations, agent.stays, agent.battery)
