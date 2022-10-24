from typing import Dict, List, Optional, Union

from Simulator import Agent, BidTracker, Environment
from ..Bids.PriorityPathBid import PriorityPathBid
from ..Bids.PrioritySpaceBid import PrioritySpaceBid


class PriorityBidTracker(BidTracker):
    """
    Tracks priority bids per tick and agent.
    Tracks the max priority per agent.
    """

    def __init__(self):
        """
        Initialize dict of bids by tick and agent.
        Initialize dict of max prio by agent.
        """
        self.past_bids: Dict[int, Dict[int, List[Union["PriorityPathBid", "PrioritySpaceBid"]]]] = {}
        self.max_bids: Dict[int, float] = {}

    def request_new_bid(self, tick: int, agent: "Agent",
                        environment: "Environment") -> Optional[Union["PriorityPathBid", "PrioritySpaceBid"]]:
        """
        Create a new bid, update the bid tracker and return the new bid.
        :param tick:
        :param agent:
        :param environment:
        :return:
        """
        if tick not in self.past_bids:
            self.past_bids[tick] = {}
        if agent not in self.past_bids[tick]:
            self.past_bids[tick][hash(agent)] = []
        new_bid: Optional[Union["PriorityPathBid", "PrioritySpaceBid"]] = agent.get_bid(tick, environment)

        if new_bid is not None and (agent not in self.max_bids or new_bid.priority > self.max_bids[hash(agent)]):
            self.max_bids[hash(agent)] = new_bid.priority
        self.past_bids[tick][hash(agent)].append(new_bid)
        return new_bid

    def get_last_bid_for_tick(self, tick: int, agent: "Agent",
                              environment: "Environment") -> Optional[Union["PriorityPathBid", "PrioritySpaceBid"]]:
        """
        Return the last bid of the tick. Creates new bid if no bid for this tick exists.
        :param tick:
        :param agent:
        :param environment:
        :return:
        """
        if tick not in self.past_bids:
            self.past_bids[tick] = {}
        if agent not in self.past_bids[tick]:
            new_bid: Optional[Union["PriorityPathBid", "PrioritySpaceBid"]] = agent.get_bid(tick, environment)
            self.past_bids[tick][hash(agent)] = [new_bid]
            if new_bid is not None and (agent not in self.max_bids or new_bid.priority > self.max_bids[hash(agent)]):
                self.max_bids[hash(agent)] = new_bid.priority
        return self.past_bids[tick][hash(agent)][-1]

    def max_prio(self, agent: "Agent") -> float:
        """
        Return the max prio of all bids of this agent.
        :param agent:
        :return:
        """
        return self.max_bids[hash(agent)]
