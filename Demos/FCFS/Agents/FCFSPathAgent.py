from Demos.FCFS.Bids.FCFSPathBid import FCFSPathBid
from Simulator import PathAgent


class FCFSPathAgent(PathAgent):
    def __init__(self,
                 locations,
                 stays,
                 simulator,
                 agent_id=None,
                 speed=None,
                 battery=None,
                 near_radius=None):
        super().__init__(locations,
                         stays,
                         simulator,
                         agent_id=agent_id,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius)

    def get_bid(self, _):
        return FCFSPathBid(self.battery, self.locations, self.stays)

    def initialize_clone(self):
        clone = FCFSPathAgent(self.locations,
                              self.stays,
                              self.simulator,
                              agent_id=self.id,
                              speed=self.speed,
                              battery=self.battery,
                              near_radius=self.near_radius)
        return clone