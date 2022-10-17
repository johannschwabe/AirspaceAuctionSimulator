from typing import Optional, TYPE_CHECKING

from API.WebClasses import WebPathBiddingStrategy
from Demos.CBS.Bids.CBSPathBid import CBSPathBid
from Demos.CBS.ValueFunction.CBSPathValueFunction import CBSPathValueFunction
from Simulator import AgentType

if TYPE_CHECKING:
    from Simulator import PathAgent, Environment


class CBSPathBiddingStrategy(WebPathBiddingStrategy):
    label = "CBS Path Bidding Strategy"
    description = "An Bidding Strategy for CBS Path Agents"
    min_locations = 2
    max_locations = 10
    allocation_type = AgentType.PATH.value

    @staticmethod
    def meta():
        return WebPathBiddingStrategy.meta()

    def generate_bid(self, agent: "PathAgent", _environment: "Environment",
                     time_step: int) -> Optional["CBSPathBid"]:
        flying = False
        locations = agent.locations
        battery = agent.battery
        stays = agent.stays
        start = None
        if len(agent.allocated_segments) > 0 and agent.allocated_segments[0].min.t <= time_step:
            index = 0
            for i, segment in enumerate(agent.allocated_segments):
                if segment.max.t >= time_step:
                    index = i
                    if segment.min.t <= time_step:
                        flying = True
                        for coordinate in segment.coordinates:
                            if coordinate.t == time_step:
                                battery -= coordinate.t - segment.min.t
                                start = coordinate.clone()
                                break
                    else:
                        start = agent.locations[i].clone()
                        start.t = max(start.t, agent.allocated_segments[i - 1].max.t) + agent.stays[i - 1]
                    break
                else:
                    battery -= segment.max.t - segment.min.t

            locations = agent.locations[index + 1:]
            locations.insert(0, start)

            stays = agent.stays[index:] if index < len(agent.stays) else []

        return CBSPathBid(agent, locations, stays, battery, flying)

    @staticmethod
    def compatible_value_functions():
        return [CBSPathValueFunction]
