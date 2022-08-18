from AAS import StationaryAgent
from Demos.FCFS.Bids.FCFSStationaryBid import FCFSStationaryBid


class FCFSStationaryAgent(StationaryAgent):

    def __init__(
        self,
        blocks,
        simulator,
        agent_id=None
    ):
        super().__init__(blocks, simulator, agent_id=agent_id)

    def get_bid(self, _):
        return FCFSStationaryBid(self.blocks)

    def initialize_clone(self):
        clone = FCFSStationaryAgent(self.blocks, self.simulator, agent_id=self.id)
        return clone
