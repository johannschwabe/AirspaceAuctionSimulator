from Mechanisms.Priority.Bids.PrioritySpaceBid import PrioritySpaceBid
from Simulator.Agents.SpaceAgent import SpaceAgent
from Simulator.Bids.BiddingStrategy import BiddingStrategy
from Simulator.Environment.Environment import Environment


class PrioritySpaceBiddingStrategy(BiddingStrategy):
    def generate_bid(self, agent: SpaceAgent, _environment: Environment, _time_step: int) -> PrioritySpaceBid:
        return PrioritySpaceBid(agent, agent.config["priority"])
