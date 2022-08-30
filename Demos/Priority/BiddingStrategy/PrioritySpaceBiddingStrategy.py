import random

from Demos.FCFS.ValueFunction.FCFSSpaceValueFunction import FCFSSpaceValueFunction
from Demos.Priority import PrioritySpaceBid
from Demos.Priority.ValueFunction.PrioritySpaceValueFunction import PrioritySpaceValueFunction
from Simulator.Agents.AgentType import AgentType
from Simulator import BiddingStrategy, SpaceAgent, Environment


class PrioritySpaceBiddingStrategy(BiddingStrategy):
    label = "Priority Space Bidding Strategy"
    description = "An Bidding Strategy for Priority Space Agents"
    min_locations = 1
    max_locations = 4
    meta = [{
        "key": "priority",
        "label": "Priority",
        "description": "Priority of the agents",
        "type": "float",
        "value": round(random.random(), 2),
    }]
    allocation_type = AgentType.SPACE.value

    def generate_bid(self, agent: "SpaceAgent", _environment: "Environment", _time_step: int) -> "PrioritySpaceBid":
        return PrioritySpaceBid(agent, agent.blocks, agent.config["priority"])

    @staticmethod
    def compatible_value_functions():
        return [PrioritySpaceValueFunction, FCFSSpaceValueFunction]
