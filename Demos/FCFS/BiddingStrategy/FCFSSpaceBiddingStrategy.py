from Demos.FCFS import FCFSSpaceBid
from Demos.FCFS.ValueFunction.FCFSSpaceValueFunction import FCFSSpaceValueFunction
from Simulator.Agents.AgentType import AgentType
from Simulator import BiddingStrategy, SpaceAgent, Environment


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
