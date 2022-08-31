from Simulator import BiddingStrategy, SpaceAgent, Environment
from ..Bids.PrioritySpaceBid import PrioritySpaceBid


class PrioritySpaceBiddingStrategy(BiddingStrategy):
    def generate_bid(self, agent: "SpaceAgent", _environment: "Environment", _time_step: int) -> "PrioritySpaceBid":
        return PrioritySpaceBid(agent, agent.blocks, agent.config["priority"])
