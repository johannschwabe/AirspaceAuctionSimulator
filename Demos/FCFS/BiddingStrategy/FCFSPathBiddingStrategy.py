from typing import TYPE_CHECKING

from API.WebClasses import WebPathBiddingStrategy
from Simulator import AgentType
from ..Bids.FCFSPathBid import FCFSPathBid
from ..ValueFunction.FCFSPathValueFunction import FCFSPathValueFunction

if TYPE_CHECKING:
    from Simulator import PathAgent, Environment


class FCFSPathBiddingStrategy(WebPathBiddingStrategy):
    label = "FCFS Path Bidding Strategy"
    description = "An Bidding Strategy for FCFS Path Agents"
    min_locations = 2
    max_locations = 10
    allocation_type = AgentType.PATH.value

    @staticmethod
    def meta():
        return WebPathBiddingStrategy.meta()

    def generate_bid(self, agent: "PathAgent", _environment: "Environment", _time_step: int) -> "FCFSPathBid":
        return FCFSPathBid(agent, agent.locations, agent.stays, agent.battery)

    @staticmethod
    def compatible_value_functions():
        return [FCFSPathValueFunction]
