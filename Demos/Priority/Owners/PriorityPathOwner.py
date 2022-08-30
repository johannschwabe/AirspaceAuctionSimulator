import random

from Simulator import PathOwner, PathAgent
from ..BiddingStrategy.PriorityPathBiddingStrategy import PriorityPathBiddingStrategy


class PriorityPathOwner(PathOwner):
    label = "Priority Path Owner"
    description = "Priority Path Owner"

    def __init__(self, owner_id, name, color, stops, creation_ticks, priority=random.random()):
        super().__init__(owner_id, name, color, stops, creation_ticks)
        self.priority = priority

    def initialize_agent(self, locations, stays, speed, battery, near_radius):
        agent_id: str = self.get_agent_id()
        bidding_strategy: "PriorityPathBiddingStrategy" = PriorityPathBiddingStrategy()
        return PathAgent(agent_id, bidding_strategy, locations, stays, config={"priority": self.priority}, speed=speed,
                         battery=battery, near_radius=near_radius)
