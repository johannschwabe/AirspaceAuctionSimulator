from typing import Dict, List, Optional, TYPE_CHECKING, Union

from Simulator import Agent, BidTracker, Environment

if TYPE_CHECKING:
    from Demos.CBS.Bids.CBSSpaceBid import CBSSpaceBid
    from Demos.CBS.Bids.CBSPathBid import CBSPathBid


class CBSBidTracker(BidTracker):
    """
    Tracks FCFS bids per tick and agent.
    """

    def __init__(self):
        """
        Initialize dict of bids by tick and agent.
        """
        self.past_bids: Dict[int, Dict["Agent", List[Union["CBSPathBid", "CBSSpaceBid"]]]] = {}

    def request_new_bid(self, tick: int, agent: "Agent",
                        environment: "Environment") -> Optional[Union["CBSPathBid", "CBSSpaceBid"]]:
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
            self.past_bids[tick][agent] = []
        new_bid: Optional[Union["CBSPathBid", "CBSSpaceBid"]] = agent.get_bid(tick, environment)
        self.past_bids[tick][agent].append(new_bid)
        return new_bid

    def get_last_bid_for_tick(self, tick: int, agent: "Agent",
                              environment: "Environment") -> Optional[Union["CBSPathBid", "CBSSpaceBid"]]:
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
            new_bid: Optional[Union["CBSPathBid", "CBSSpaceBid"]] = agent.get_bid(tick, environment)
            self.past_bids[tick][agent] = [new_bid]
        return self.past_bids[tick][agent][-1]
