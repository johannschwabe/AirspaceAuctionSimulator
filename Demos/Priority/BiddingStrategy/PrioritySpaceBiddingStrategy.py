from Demos.Priority import PrioritySpaceBid
from Simulator import BiddingStrategy, SpaceAgent, Environment


class PrioritySpaceBiddingStrategy(BiddingStrategy):
    def generate_bid(self, agent: "SpaceAgent", _environment: "Environment", _time_step: int) -> "PrioritySpaceBid":
        return PrioritySpaceBid(agent, agent.blocks, agent.config["priority"])
