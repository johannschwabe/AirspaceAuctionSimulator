from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Simulator.Agents.Agent import Agent
    from Simulator.Bids.Bid import Bid
    from Simulator.Environment.Environment import Environment


class BidTracker(ABC):
    """
    Tracks priority bids per tick and agent.
    """

    @abstractmethod
    def get_last_bid_for_tick(self, tick: int, agent: "Agent", environment: "Environment") -> Optional["Bid"]:
        """
        Return the last bid of the tick. Creates new bid if no bid for this tick exists.
        :param tick:
        :param agent:
        :param environment:
        :return:
        """
        pass

    @abstractmethod
    def request_new_bid(self, tick: int, agent: "Agent", environment: "Environment") -> Optional["Bid"]:
        """
        Create a new bid, update the bid tracker and return the new bid.
        :param tick:
        :param agent:
        :param environment:
        :return:
        """
        pass
