from Simulator import PathAgent
from ..Bids.FCFSPathBid import FCFSPathBid


class FCFSPathAgent(PathAgent):
    def __init__(self,
                 agent_id,
                 locations,
                 stays,
                 speed=None,
                 battery=None,
                 near_radius=None,
                 _is_clone=False):
        super().__init__(agent_id,
                         locations,
                         stays,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius,
                         _is_clone=_is_clone)

    def get_bid(self, _):
        return FCFSPathBid(self.battery, self.locations, self.stays)

    def initialize_clone(self):
        clone = FCFSPathAgent(self.id,
                              self.locations,
                              self.stays,
                              speed=self.speed,
                              battery=self.battery,
                              near_radius=self.near_radius,
                              _is_clone=True)
        return clone
