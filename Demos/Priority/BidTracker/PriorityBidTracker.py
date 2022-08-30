from typing import Dict, List, Optional

from Simulator.Agents.Agent import Agent
from Simulator.BidTracker.BidTracker import BidTracker
from Simulator.Bids.Bid import Bid
from Simulator.Environment.Environment import Environment


class PriorityBidTracker(BidTracker):
    def __init__(self):
        super().__init__()
        self.past_bids: Dict[int, Dict[Agent, List[Bid]]] = {}
        self.max_bids: Dict[Agent, float] = {}

    def request_new_bid(self, tick: int, agent: Agent, environment: Environment) -> Optional[Bid]:
        if tick not in self.past_bids:
            self.past_bids[tick] = {}
        if agent not in self.past_bids[tick]:
            self.past_bids[tick][agent] = []
        new_bid = agent.get_bid(tick, environment)

        if new_bid is not None and (agent not in self.max_bids or new_bid.priority > self.max_bids[agent]):
            self.max_bids[agent] = new_bid.priority
        self.past_bids[tick][agent].append(new_bid)
        return new_bid

    def get_last_bid_for_tick(self, tick: int, agent: Agent, environment: Environment) -> Optional[Bid]:
        if tick not in self.past_bids:
            self.past_bids[tick] = {}
        if agent not in self.past_bids[tick]:
            new_bid = agent.get_bid(tick, environment)
            self.past_bids[tick][agent] = [new_bid]
            if new_bid is not None and (agent not in self.max_bids or new_bid.priority > self.max_bids[agent]):
                self.max_bids[agent] = new_bid.priority
        return self.past_bids[tick][agent][-1]

    def max_prio(self, agent: Agent) -> float:
        return self.max_bids[agent]
