from typing import TYPE_CHECKING

from Simulator.Agents.AgentType import AgentType
from ..ValueFunction.FCFSPathValueFunction import FCFSPathValueFunction

if TYPE_CHECKING:
    from Simulator import PathAgent, Environment
from Simulator import BiddingStrategy, PathAgent, Environment
from ..Bids.FCFSPathBid import FCFSPathBid


class FCFSPathBiddingStrategy(BiddingStrategy):
    label = "FCFS Path Bidding Strategy"
    description = "An Bidding Strategy for FCFS Path Agents"
    min_locations = 2
    max_locations = 5
    meta = []
    allocation_type = AgentType.PATH.value

    def generate_bid(self, agent: "PathAgent", _environment: "Environment", _time_step: int) -> "FCFSPathBid":
        return FCFSPathBid(agent, agent.locations, agent.stays, agent.battery)

    @staticmethod
    def compatible_value_functions():
        return [FCFSPathValueFunction]
