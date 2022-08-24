from Simulator import SpaceAgent
from ..Bids.PrioritySpaceBid import PrioritySpaceBid


class PrioritySpaceAgent(SpaceAgent):
    def __init__(self,
                 agent_id,
                 blocks,
                 priority,
                 _is_clone=False):
        super().__init__(agent_id, blocks)
        self.priority = priority

    def get_bid(self, t: int):
        return PrioritySpaceBid(self.blocks, self.priority)

    def initialize_clone(self):
        clone = PrioritySpaceAgent(self.id, self.blocks, self.priority, _is_clone=True)
        return clone
