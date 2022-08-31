from typing import Dict, List, Optional

from Simulator import BidTracker, Agent, Bid, Environment


class FCFSBidTracker(BidTracker):
    def __init__(self):
        super().__init__()
        self.past_bids: Dict[int, Dict["Agent", List["Bid"]]] = {}

    def request_new_bid(self, tick: int, agent: "Agent", environment: "Environment") -> Optional["Bid"]:
        if tick not in self.past_bids:
            self.past_bids[tick] = {}
        if agent not in self.past_bids[tick]:
            self.past_bids[tick][agent] = []
        new_bid = agent.get_bid(tick, environment)
        self.past_bids[tick][agent].append(new_bid)
        return new_bid

    def get_last_bid_for_tick(self, tick: int, agent: "Agent", environment: "Environment") -> Optional["Bid"]:
        if tick not in self.past_bids:
            self.past_bids[tick] = {}
        if agent not in self.past_bids[tick]:
            new_bid = agent.get_bid(tick, environment)
            self.past_bids[tick][agent] = [new_bid]
        return self.past_bids[tick][agent][-1]
