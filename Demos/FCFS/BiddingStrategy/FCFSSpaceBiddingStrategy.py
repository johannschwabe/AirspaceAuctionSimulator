from typing import TYPE_CHECKING

from Simulator.Agents.AgentType import AgentType
from ..ValueFunction.FCFSSpaceValueFunction import FCFSSpaceValueFunction

if TYPE_CHECKING:
    from Simulator import SpaceAgent, Environment
from Simulator import BiddingStrategy, SpaceAgent, Environment
from ..Bids.FCFSSpaceBid import FCFSSpaceBid


class FCFSSpaceBiddingStrategy(BiddingStrategy):
    label = "FCFS Space Bidding Strategy"
    description = "An Bidding Strategy for FCFS Space Agents"
    min_locations = 1
    max_locations = 4
    meta = []
    allocation_type = AgentType.SPACE.value

    def generate_bid(self, agent: "SpaceAgent", _environment: "Environment", _time_step: int) -> "FCFSSpaceBid":
        return FCFSSpaceBid(agent, agent.blocks)

    @staticmethod
    def compatible_value_functions():
        return [FCFSSpaceValueFunction]
