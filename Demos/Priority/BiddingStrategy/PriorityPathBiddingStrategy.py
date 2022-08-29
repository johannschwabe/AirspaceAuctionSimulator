from Demos.Priority.Bids.PriorityPathBid import PriorityPathBid
from Simulator.Agents.AgentType import AgentType
from Simulator.Agents.PathAgent import PathAgent
from Simulator.Bids.BiddingStrategy import BiddingStrategy
from Simulator.Environment.Environment import Environment


class PriorityPathBiddingStrategy(BiddingStrategy):
    label = "Priority Path Bidding Strategy"
    description = "An Bidding Strategy for Priority Path Agents"
    min_locations = 2
    max_locations = 5
    meta = []
    allocation_type = AgentType.PATH.value

    def generate_bid(self, agent: PathAgent, _environment: Environment, time_step: int) -> PriorityPathBid:
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
                    if segment.min.t < time_step:
                        flying = True
                        for coordinate in segment.coordinates:
                            if coordinate.t == time_step:
                                start = coordinate.clone()
                    else:
                        start = agent.allocated_segments[i - 1].max.clone()
                        start.t += agent.stays[i - 1]
                    break
            if start is None:
                raise Exception(f"Invalid segments allocated at tick {time_step}: {agent.allocated_segments}")

            locations = agent.locations[index + 1:]
            locations.insert(0, start)

            stays = agent.stays[index:] if index < len(agent.stays) else []

        return PriorityPathBid(agent, locations, stays, battery, agent.config["priority"], flying)
