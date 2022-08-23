from Demos.Priority.Bids.PrioritySpaceBid import PrioritySpaceBid
from Simulator import SpaceAgent


class PrioritySpaceAgent(SpaceAgent):
    def __init__(
        self,
        blocks,
        priority,
        simulator,
        agent_id=None
    ):
        super().__init__(blocks, simulator, agent_id=agent_id)
        self.priority = priority

    def get_bid(self, t: int):
        return PrioritySpaceBid(self.blocks, self.priority)

    def initialize_clone(self):
        clone = PrioritySpaceAgent(self.blocks, self.priority, self.simulator, agent_id=self.id)
        return clone
