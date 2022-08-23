from Demos.FCFS.Bids.FCFSSpaceBid import FCFSSpaceBid
from Simulator import SpaceAgent


class FCFSSpaceAgent(SpaceAgent):

    def __init__(self,
                 blocks,
                 simulator,
                 agent_id=None):
        super().__init__(blocks, simulator, agent_id=agent_id)

    def get_bid(self, _):
        return FCFSSpaceBid(self.blocks)

    def initialize_clone(self):
        clone = FCFSSpaceAgent(self.blocks, self.simulator, agent_id=self.id)
        return clone
