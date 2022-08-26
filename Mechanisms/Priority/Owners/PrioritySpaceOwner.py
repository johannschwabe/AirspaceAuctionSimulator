import random

from Mechanisms.Priority.BiddingStrategy.PrioritySpaceBiddingStrategy import PrioritySpaceBiddingStrategy
from Simulator import SpaceOwner, Coordinate4D
from Simulator.Agents.SpaceAgent import SpaceAgent


class PrioritySpaceOwner(SpaceOwner):
    label = "Priority Space Owner"
    description = "Priority Space Owner"

    def __init__(self, owner_id, name, color, stops, creation_ticks, size=Coordinate4D(20, 20, 20, 200),
                 priority=random.random()):
        super().__init__(owner_id, name, color, stops, creation_ticks, size)
        self.priority = priority

    def initialize_agent(self, blocks):
        agent_id: str = self.get_agent_id()
        bidding_strategy: "PrioritySpaceBiddingStrategy" = PrioritySpaceBiddingStrategy()
        return SpaceAgent(agent_id, bidding_strategy, blocks, config={"priority": self.priority})
