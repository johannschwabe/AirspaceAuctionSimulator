from typing import TYPE_CHECKING

from Demos.CBS.Bids.CBSPathBid import CBSPathBid
from Demos.CBS.ValueFunction.CBSPathValueFunction import CBSPathValueFunction
from Simulator import AgentType, BiddingStrategy
from Simulator.Bids.PathBiddingStrategy import PathBiddingStrategy

if TYPE_CHECKING:
    from Simulator import PathAgent, Environment


class CBSPathBiddingStrategy(BiddingStrategy, PathBiddingStrategy):
    label = "CBS Path Bidding Strategy"
    description = "An Bidding Strategy for CBS Path Agents"
    min_locations = 2
    max_locations = 5
    allocation_type = AgentType.PATH.value

    @staticmethod
    def meta():
        return PathBiddingStrategy.meta()

    def generate_bid(self, agent: "PathAgent", _environment: "Environment", _time_step: int) -> "CBSPathBid":
        return CBSPathBid(agent, agent.locations, agent.stays, agent.battery)

    @staticmethod
    def compatible_value_functions():
        return [CBSPathValueFunction]
