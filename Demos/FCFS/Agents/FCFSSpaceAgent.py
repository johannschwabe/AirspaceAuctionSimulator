from Simulator import SpaceAgent
from ..Bids.FCFSSpaceBid import FCFSSpaceBid


class FCFSSpaceAgent(SpaceAgent):

    def __init__(self, agent_id, blocks, _is_clone=False):
        super().__init__(agent_id, blocks, _is_clone=_is_clone)

    def get_bid(self, _):
        return FCFSSpaceBid(self.blocks)

    def initialize_clone(self):
        clone = FCFSSpaceAgent(self.id, self.blocks, _is_clone=True)
        return clone
