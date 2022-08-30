from Demos.FCFS.Bids.FCFSSpaceBid import FCFSSpaceBid
from Demos.FCFS.ValueFunction.FCFSSpaceValueFunction import FCFSSpaceValueFunction
from Simulator.Agents.AgentType import AgentType
from Simulator.Agents.SpaceAgent import SpaceAgent
from Simulator.Bids.BiddingStrategy import BiddingStrategy
from Simulator.Environment.Environment import Environment


class FCFSSpaceBiddingStrategy(BiddingStrategy):
    label = "FCFS Space Bidding Strategy"
    description = "An Bidding Strategy for FCFS Space Agents"
    min_locations = 1
    max_locations = 4
    meta = []
    allocation_type = AgentType.SPACE.value

    def generate_bid(self, agent: SpaceAgent, _environment: Environment, _time_step: int) -> FCFSSpaceBid:
        return FCFSSpaceBid(agent)

    @staticmethod
    def compatible_value_functions():
        return [FCFSSpaceValueFunction]
