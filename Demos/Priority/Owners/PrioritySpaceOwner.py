import random

from Simulator import SpaceOwner, SpaceAgent
from ..BiddingStrategy.PrioritySpaceBiddingStrategy import PrioritySpaceBiddingStrategy


class PrioritySpaceOwner(SpaceOwner):
    label = "Priority Space Owner"
    description = "Priority Space Owner"

    def __init__(self, owner_id, name, color, stops, creation_ticks, size, priority=random.random()):
        super().__init__(owner_id, name, color, stops, creation_ticks, size)
        self.priority = priority

    def initialize_agent(self, blocks):
        agent_id: str = self.get_agent_id()
        bidding_strategy: "PrioritySpaceBiddingStrategy" = PrioritySpaceBiddingStrategy()
        return SpaceAgent(agent_id, bidding_strategy, blocks, config={"priority": self.priority})
