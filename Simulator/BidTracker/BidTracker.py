from abc import ABC, abstractmethod
from typing import Optional

from Simulator.Agents.Agent import Agent
from Simulator.Bids.Bid import Bid
from Simulator.Environment.Environment import Environment


class BidTracker(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_last_bid_for_tick(self, tick: int, agent: "Agent", environment: "Environment") -> Optional["Bid"]:
        pass

    @abstractmethod
    def request_new_bid(self, tick: int, agent: Agent, environment: Environment) -> Optional["Bid"]:
        pass
