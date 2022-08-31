from Simulator import BiddingStrategy, SpaceAgent, Environment
from ..Bids.FCFSSpaceBid import FCFSSpaceBid


class FCFSSpaceBiddingStrategy(BiddingStrategy):
    def generate_bid(self, agent: "SpaceAgent", _environment: "Environment", _time_step: int) -> "FCFSSpaceBid":
        return FCFSSpaceBid(agent, agent.blocks)
