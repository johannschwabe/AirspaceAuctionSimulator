import random
from typing import TYPE_CHECKING

from API import WebSpaceBiddingStrategy
from Simulator import AgentType
from ..Bids.PrioritySpaceBid import PrioritySpaceBid
from ..ValueFunction.PrioritySpaceValueFunction import PrioritySpaceValueFunction
from ...FCFS.ValueFunction.FCFSSpaceValueFunction import FCFSSpaceValueFunction

if TYPE_CHECKING:
    from Simulator import SpaceAgent, Environment


class PrioritySpaceBiddingStrategy(WebSpaceBiddingStrategy):
    label = "Priority Space Bidding Strategy"
    description = "An Bidding Strategy for Priority Space Agents"
    min_locations = 1
    max_locations = 4
    allocation_type = AgentType.SPACE.value

    @staticmethod
    def meta():
        return [
            *WebSpaceBiddingStrategy.meta(),
            {
                "key": "priority",
                "label": "Priority",
                "description": "Priority of the agents",
                "type": "float",
                "value": round(random.random(), 2),
                "range": "0-1"
            }
        ]

    def generate_bid(self, agent: "SpaceAgent", _environment: "Environment", _time_step: int) -> "PrioritySpaceBid":
        return PrioritySpaceBid(agent, agent.blocks, agent.config["priority"])

    @staticmethod
    def compatible_value_functions():
        return [PrioritySpaceValueFunction, FCFSSpaceValueFunction]
