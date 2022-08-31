from typing import Optional

from Simulator import BiddingStrategy, PathAgent, Environment
from ..Bids.PriorityPathBid import PriorityPathBid


class PriorityPathBiddingStrategy(BiddingStrategy):
    def generate_bid(self, agent: "PathAgent", _environment: "Environment",
                     time_step: int) -> Optional["PriorityPathBid"]:
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
                    else:
                        start = agent.locations[i].clone()
                        start.t = max(start.t, agent.allocated_segments[i - 1].max.t) + agent.stays[i - 1]
                    break
                else:
                    battery -= segment.max.t - segment.min.t
            if start is None:
                print(f"Agent {agent} crashed.")
                return None

            locations = agent.locations[index + 1:]
            locations.insert(0, start)

            stays = agent.stays[index:] if index < len(agent.stays) else []

        return PriorityPathBid(agent, locations, stays, battery, agent.config["priority"], flying)
