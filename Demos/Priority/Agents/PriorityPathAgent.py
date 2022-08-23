from Demos.Priority.Bids.PriorityPathBid import PriorityPathBid
from Simulator import PathAgent


class PriorityPathAgent(PathAgent):
    def __init__(self,
                 locations,
                 priority,
                 simulator,
                 stays,
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
        self.priority = priority

    def get_bid(self, t: int):
        flying = False  # TODO
        return PriorityPathBid(self.battery, self.locations, self.stays, self.priority, flying)

    def initialize_clone(self):
        clone = PriorityPathAgent(self.locations,
                                  self.priority,
                                  self.simulator,
                                  self.stays,
                                  agent_id=self.id,
                                  speed=self.speed,
                                  battery=self.battery,
                                  near_radius=self.near_radius)
        return clone
