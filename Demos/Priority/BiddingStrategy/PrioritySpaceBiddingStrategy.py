import random

from Demos.FCFS.ValueFunction.FCFSSpaceValueFunction import FCFSSpaceValueFunction
from Demos.Priority.Bids.PrioritySpaceBid import PrioritySpaceBid
from Demos.Priority.ValueFunction.PrioritySpaceValueFunction import PrioritySpaceValueFunction
from Simulator.Agents.AgentType import AgentType
from Simulator.Agents.SpaceAgent import SpaceAgent
from Simulator.Bids.BiddingStrategy import BiddingStrategy
from Simulator.Environment.Environment import Environment


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

    def generate_bid(self, agent: SpaceAgent, _environment: Environment, _time_step: int) -> PrioritySpaceBid:
        return PrioritySpaceBid(agent, agent.config["priority"])

    @staticmethod
    def compatible_value_functions():
        return [PrioritySpaceValueFunction, FCFSSpaceValueFunction]
