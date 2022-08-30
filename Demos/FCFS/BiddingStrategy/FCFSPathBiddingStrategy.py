from Demos.FCFS import FCFSPathBid
from Simulator import BiddingStrategy, PathAgent, Environment


class FCFSPathBiddingStrategy(BiddingStrategy):
    def generate_bid(self, agent: "PathAgent", _environment: "Environment", _time_step: int) -> "FCFSPathBid":
        return FCFSPathBid(agent, agent.locations, agent.stays, agent.battery)
