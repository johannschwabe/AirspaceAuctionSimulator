from typing import TYPE_CHECKING

from API.WebClasses import WebSpaceBiddingStrategy
from Simulator import AgentType
from ..Bids.FCFSSpaceBid import FCFSSpaceBid
from ..ValueFunction.FCFSSpaceValueFunction import FCFSSpaceValueFunction

if TYPE_CHECKING:
    from Simulator import SpaceAgent, Environment


class FCFSSpaceBiddingStrategy(WebSpaceBiddingStrategy):
    label = "FCFS Space Bidding Strategy"
    description = "An Bidding Strategy for FCFS Space Agents"
    min_locations = 1
    max_locations = 4
    allocation_type = AgentType.SPACE.value

    @staticmethod
    def meta():
        return WebSpaceBiddingStrategy.meta()

    def generate_bid(self, agent: "SpaceAgent", _environment: "Environment", _time_step: int) -> "FCFSSpaceBid":
        return FCFSSpaceBid(agent, agent.blocks)

    @staticmethod
    def compatible_value_functions():
        return [FCFSSpaceValueFunction]
